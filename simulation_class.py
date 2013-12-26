import datetime
import time
from chart_class import *
from bar_class import *
from moving_average_class import *
from order_class import *
from Tkinter import *
import tkMessageBox
from stochastic_oscillator_class import *

pip_representation = {'EURUSD': 0.0001, 'GBPUSD': 0.0001, \
                      'USDCHF': 0.0001, 'USDJPY':0.01}
spread_dict = {'EURUSD':.00026, 'GBPUSD':.00027, 'USDJPY':.024, 'USDCHF':.00026}
class Simulation(object):
    #pass through the dictionary of user input and the newchart 
    def __init__(self, parameters_dict, chart):
        self.parameters_dict = parameters_dict
        self.chart = chart
        self.results = {}
        self.open_orders = []
        self.closed_orders = []
        self.balance = parameters_dict['Deposit']
        self.margin = 0 #initially
        self.base_currency = parameters_dict['Symbol'][0:3]
        self.quote_currency = parameters_dict['Symbol'][3:]
        self.symbol = parameters_dict['Symbol']
        self.equity = self.balance * parameters_dict['MaxMargin']
        self.free_margin = self.equity - self.margin
        """as orders are opened, depending on open positions' profit/loss, and
        adds to the account balance, and the used margin by the open positions,
        the free margin can be calculated."""
        """def of free margin = Equity - Margin
        ex:)inputs: balance = 1,000, max margin: 0.1, one position with
        total margin of $9000 and profit of $4000
        Equity = 1,000 * 10 + 4000
        Margin = 9000
        Free Margin = Equity - Margin = 10,000 + 4000 - 9000 = 5000"""
    def getStrategy(self):
        #return an instance of the strategy selected by user
        if self.parameters_dict['TradingCriterium'] == \
           'Moving Average CrossOver':
            return MovingAverageStrategy(self.chart)
        elif self.parameters_dict['TradingCriterium'] == \
        'Stochastic Oscillator':
            return StochasticOscillatorStrategy(self.chart) 
    def okShort(self): #return boolean
        if self.parameters_dict['Position'] == 'Only Short':
            return True
        elif self.parameters_dict['Position'] == 'Include Both':
            return True
        return False
    def okLong(self): #return boolean
        if self.parameters_dict['Position'] == 'Only Long':
            return True
        elif self.parameters_dict['Position'] == 'Include Both':
            return True
        return False
    
    def calculateMargin(self, bar, lots, leverage):
        if self.quote_currency == 'USD':
            return 100000 * lots / leverage
        else:
            return bar.getCloseValue() *lots*100000/ leverage
            
    def openOrder(self, bar, position):
        #subtract free margin after each order
        #update equity 
        open_time_of_order = bar.endTimeOfBar
        lots = self.getLots(bar)
        if self.getLots(bar) == False:
            return False #return to user 'You blew your account.'
        currency_pair = self.parameters_dict['Symbol']
        open_price = self.getOpenPrice(currency_pair,bar,position)
        stop_loss = self.getStopLoss(bar,position,currency_pair)
        take_profit = self.getTakeProfit(bar,position,currency_pair)
        margin = self.calculateMargin(bar,lots,\
                                      self.parameters_dict['MaxMargin'])
        self.margin += margin
        self.free_margin = self.equity - self.margin
        openorder = Order(open_time_of_order, lots, currency_pair, \
                          open_price, stop_loss,take_profit,\
                          position, margin)
        self.open_orders.append(openorder)

    def getOpenPrice(self, symbol,bar,position):
        if position == 'Short':
            return bar.getCloseValue()
        elif position == 'Long':
            #need to account for spread
            spread = spread_dict[symbol]
            return bar.getCloseValue() + spread

    def getStopLoss(self, bar, position, symbol):
        stop_loss_option = self.parameters_dict['TradeManag']
        pip_value = pip_representation[symbol]
        if 'Take Profit Stop-Loss' in stop_loss_option:
            #fixed take profit and stop loss values chosen
            slpips = self.parameters_dict['StopLoss']
            slvalue = pip_value * float(slpips)
            if position == 'Long':
                return bar.getCloseValue() - slvalue
            elif position == 'Short':
                return bar.getCloseValue() + slvalue
        else:
            #price percentage trailing deviation stop loss
            pippercent = self.parameters_dict['PricePercent']
            sldeviation = (bar.getCloseValue())*(float(pippercent)/100)
            if position == 'Long':
                return bar.getCloseValue() - sldeviation
            elif position == 'Short':
                return bar.getCloseValue() + sldeviation
        return 0

    def getTakeProfit(self,bar,position,symbol):
        take_profit_option = self.parameters_dict['TradeManag']
        pip_value = pip_representation[symbol]
        if 'Take Profit Stop Loss' in take_profit_option:
            #take profit pip level is chosen by the user
            tppips = self.parameters_dict['TakeProfit']
            tpvalue = (pip_value * tppips)
            if position == 'Long':
                return bar.getCloseValue() + tpvalue
            elif position == 'Short':
                return bar.getCloseValue() - tpvalue
        return 0
    
    #this function returns the appropriate lot size based upon the constraints
    def getLots(self,bar):
        user_lot_input = float(self.parameters_dict['LotSize'])
        #find out first how much the lot size is in the quote currency, \
        #then convert to corresponding
        #USD
        if self.free_margin == 0:
            return False
        if self.quote_currency == 'USD':
            proposed_value_of_order = (user_lot_input * 100000)
            if proposed_value_of_order > self.free_margin:
                #find the max lot size below the user's input
                return (self.free_margin)/(100000)
            else:
                return user_lot_input
        else: #self.quote_currency != 'USD'
            #USD is base currency, but foreign currency is the quote currency
            usd_equivalent_value_of_lot = ((user_lot_input * 100000)*\
                                           (bar.getCloseValue()))
            if usd_equivalent_value_of_lot > self.free_margin:
                return (self.free_margin)/(100000)
            else:
                return user_lot_input
            
    def manageOpenOrders(self,bar,symbol):
        #this only is for the Price Percent Stop Loss
        if 'Price % Stop-Loss' in self.parameters_dict['TradeManag']:
            for openorder in self.open_orders:
                slnewpercent = self.getStopLoss(bar,openorder.getPosition(),\
                                                symbol)
                openorder.updateStopLoss(slnewpercent)

    def closeOrders(self, currentbar):
        if len(self.open_orders) == 0:
            return
        else:
            #close order if order's take profit or stop loss has been hit
            for order in self.open_orders:
                #check if order hit Take Profit
                if currentbar.isInBar(order.getTakeProfit()):
                    order.closeOrder(order.getTakeProfit())
                    order.calculateProfit(currentbar)
                #check if order hit Stop Loss
                elif currentbar.isInBar(order.getStopLoss()):
                    order.closeOrder(order.getStopLoss())
                    order.calculateProfit(currentbar)
            #add these to closed orders
            new_closed_orders = [order for order in self.open_orders \
                                 if order.isClosed == True]
            #list comprehensions
            self.closed_orders += new_closed_orders
            difference_set = set(new_closed_orders)
            self.open_orders = [order for order in self.open_orders \
                                if order not in difference_set]
            #figures out how much free margin is left after the order is \
            #closed and update account 
            #balance:
            for new_closed_order in new_closed_orders:
                profit = new_closed_order.calculateProfit(currentbar)
                self.balance += profit
                self.equity += profit
                self.margin += new_closed_order.margin_consumed
                self.free_margin = self.equity - self.margin

    def closeRemainingOrders(self,lastbar):
        for order in self.open_orders:
            order.closeOrder(lastbar.getCloseValue())
            order.calculateProfit(lastbar)
        #done testing
        new_closed_orders = self.open_orders
        #list comprehensions
        self.closed_orders += new_closed_orders
        difference_set = set(new_closed_orders)
        self.open_orders = [order for order in self.open_orders \
                            if order not in difference_set]
        #figure out how much free margin is left after the order is \
        #closed and update account balance:
        for new_closed_order in new_closed_orders:
            profit = new_closed_order.calculateProfit(lastbar)
            self.balance += profit
            self.equity += profit
            self.margin += new_closed_order.margin_consumed
            self.free_margin = self.equity - self.margin
                
    def updateEquity(self, bar):
        for openorder in self.open_orders:
            unrealized_profit = openorder.calculateProfit(bar)
            self.equity += unrealized_profit

    def runSimulation(self):
        #run a for loop through all bars of the new chart
        #find out what trade criteria desired - MA or Stochastic Oscillator
        # for opening the order:
        strategy = self.getStrategy()
        okshort  = self.okShort()
        oklong = self.okLong()
        strategy.calculateIndicator() #changes its state internally
        buyorderindexes = strategy.getBuySignals()
        sellorderindexes = strategy.getSellSignals()

        #enumerate so that we not only get the bar but the index as well
        for index,eachbar in enumerate(self.chart.getBarsList()):
            self.closeOrders(eachbar)
            self.updateEquity(eachbar)
            if okshort:
                if index in sellorderindexes:
                    self.openOrder(eachbar, 'Short')
            if oklong:
                if index in buyorderindexes:
                    self.openOrder(eachbar, 'Long')
            self.manageOpenOrders(eachbar,self.symbol)
        self.closeRemainingOrders(self.chart.getBarsList()[-1])

    def getClosedOrders(self):
        return self.closed_orders

    def getOverallBalance(self):
        return str(format(self.balance,'.2f'))

    def getOverallProfit(self):
        overall_profit = self.balance-self.parameters_dict['Deposit']
        return str(format(overall_profit,'.2f'))

    def getOverallEquity(self):
        return str(format(self.balance,'.2f'))
        

    """def graphSimulation(self):
        try:
            dataFile = self.symbol + '.csv'
            loaded_data = np.loadtxt(self.symbol + '.csv')

            candlestick(ax1, DATA, width
        
            
    if self.parameters_dict['TradingCriterium'] == 'Only Short':
            #check if you have enough free margin
            #only short, the lot size indicated, if not try next smaller lot
        if self.parameters_dict['TradingCriterium'] == 'Only Long':
            #check if you have enough free margin
            #only long, the lot size indicated, if not try next smaller lot
        if self.parameters_dict['TradingCriterium'] == 'Include Both'
            #check if you have enough free margin
            #do both sell and buy orders, if not find the right one
        # for closing the order:
        if self.parameters_dict['Trailing'] == self.chart[i].
            self.parameters_dict['TakeProfit'] == self.chart[i].
            self.parameters_dict['StopLoss'] == self.chart[i].
            self.parameters_dict['PricePercent'] == self.chart[i].
        #automatically close all open orders at last bar
        #return the user balance and list of all orders that were created.
        
    def graphSimulation(self, parameters_dict, chart):
        #draw regular chart
        #draw lines to represent the trading strategy, possibly color-code
        #based upon the type of order that was executed at that bar"""
            
