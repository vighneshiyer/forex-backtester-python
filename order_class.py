#standard definition for pip is 1/100th of a percent for all major currency
#paris, with the exception of the yen, or in our case USDJPY. Ten is only
#quoted up to two decimal places
pip_representation = {'EURUSD': 0.0001, 'GBPUSD': 0.0001, \
                      'USDCHF': 0.0001, 'USDJPY':0.01}
class Order(object):    
    def __init__(self, order_open_time, lots, symbol,order_open_price, \
                 initial_stop_loss, initial_take_profit, \
                 position, margin):
        self.order_open_time = order_open_time
        self.order_lots = lots
        self.symbol = symbol
        self.base_currency = symbol[0:3]
        self.quote_currency = symbol[3:]
        self.position = position
        self.order_open_price = order_open_price
        self.stop_loss = initial_stop_loss
        self.take_profit = initial_take_profit
        self.order_close_price = None
        self.margin_consumed = margin
        self.profit = None
        self.isClosed = False
    def __repr__(self):
        order_summary = ''
        order_summary +=('Order Opened At This Date & Time:' + ' ' + \
                         str(self.order_open_time) +'\t')
        order_summary +=( 'Order Opened At This Price:' + ' ' +\
                         str(self.order_open_price)+'\t')
        order_summary += ('Order Closed At This Price:' + ' ' + \
                         str(self.order_close_price)+'\t')
        order_summary += ('Order Consumed This Much Margin:' + ' ' + \
                         str(format(self.margin_consumed,'.2f'))+'\t')
        order_summary +=('Order Profit/Loss:'+' '+str(format(self.profit,'.2f'))\
                                                      +' USD'+'\t')
        order_summary += ('\n')
        return order_summary
    def getPosition(self):
        return self.position
    def getTakeProfit(self):
        return self.take_profit
    def getStopLoss(self):
        return self.stop_loss
    
    def closeOrder(self, closeprice):
        if self.isClosed == True:
            raise RuntimeError('Cannot Close An Already Closed Order!')
        self.order_close_price = closeprice
        self.isClosed = True
        
    def calculateProfit(self, currentbar): 
        pip_value = pip_representation[self.symbol] 
        if self.isClosed == True: 
            if self.quote_currency == 'USD': 
                self.profit = (self.order_close_price - \
                               self.order_open_price)*self.order_lots*100000
                return self.profit 
            elif self.quote_currency != 'USD': 
                self.profit = (self.order_close_price -self.order_open_price)*\
                              currentbar.getCloseValue()*self.order_lots*100000
                return self.profit
            
        else: #reached the end of testing period, but some orders are still open
            #close the remaining open orders so we can calculate profit
            if currentbar != None: 
                if self.quote_currency == 'USD': 
                    self.profit = (currentbar.getCloseValue()- \
                                   self.order_open_price)*self.order_lots*100000
                    return self.profit 
                elif self.quote_currency != 'USD': 
                    self.profit = (currentbar.getCloseValue() - \
                                   self.order_open_price)*\
                                   currentbar.getCloseValue()*\
                                   self.order_lots*100000
                    return self.profit
                
    def updateStopLoss(self, newstoploss):
        self.stop_loss = newstoploss
