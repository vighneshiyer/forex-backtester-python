from Tkinter import *
from bar_class import *
from chart_class import *
from csv_parser import *
from simulation_class import *
import tkMessageBox
import datetime
import time

root = Tk()
inputs = {} #initalize dict that maps the name of parameter to pointer
parameters = {} #initialize dict that maps the name of parameter to user entry
#historical data time period that is available for user to test against
start_date_availability = datetime.datetime(2013,1,1) 
end_date_availability = datetime.datetime(2013,11,22)
#today's current day
today_date = datetime.datetime.today()

#Program Name SetUp
ProgramNameLabel = Label(root, text = 'Forex Backtesting Simulation Program',\
                         font= 'Times 20 bold', fg = 'red')
ProgramNameLabel.pack()

#Start Date SetUp
StartDateLabel = Label(root, text = 'Start Date (MM/DD/YYYY)')
StartDateLabel.pack()
StartDateEntry = Entry(root, bd = 15)
StartDateEntry.pack()
inputs['StartDate'] = StartDateEntry

#End Date SetUp
EndDateLabel = Label(root, text = 'End Date (MM/DD/YYYY)')
EndDateLabel.pack()
EndDateEntry = Entry(root, bd = 15)
EndDateEntry.pack()
inputs['EndDate'] = EndDateEntry

#Initial Deposit SetUp
DepositLabel = Label(root, text = 'Initial Deposit (USD)')
DepositLabel.pack()
DepositEntry = Entry(root, bd = 15)
DepositEntry.pack()
inputs['Deposit'] = DepositEntry

#Time Frame SetUp
TimeFrameVar = StringVar()
TimeFrameVar.set('TimeFrame')
OptionMenu(root, TimeFrameVar,'M1(1 Minute)','M5(5 Minutes)','M15(15 Minutes)',\
           'M30(30 Minutes)','H1(1 Hour)','H4(4 Hours)','D1(1 Day)',\
           'W1(1 Week)').pack()
inputs['TimeFrame'] = TimeFrameVar

#Symbol SetUp
SymbolVar = StringVar()
SymbolVar.set('Symbol')
OptionMenu(root, SymbolVar, 'EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF').pack()
inputs['Symbol'] = SymbolVar

#Position SetUp
PositionVar = StringVar()
PositionVar.set('Position To Trade')
OptionMenu(root, PositionVar, 'Only Short','Only Long','Include Both').pack()
inputs['Position'] = PositionVar

#Trading Criterium SetUp
TradeVar = StringVar()
TradeVar.set('Trading Criterium')
OptionMenu(root, TradeVar,'Moving Average CrossOver', 'Stochastic Oscillator')\
                 .pack()
inputs['TradingCriterium'] = TradeVar

#Max Margin SetUp
MaxMarginVar = StringVar()
MaxMarginVar.set('Max Margin Ratio')
OptionMenu(root, MaxMarginVar,'1:10','1:20','1:50','1:100','1:500','1:1000').\
                 pack()
inputs['MaxMargin'] = MaxMarginVar

#Preferred Lot-Size SetUp
LotSizeVar = StringVar()
LotSizeVar.set('Preferred Lot Size')
OptionMenu(root, LotSizeVar, '0.01','0.05','0.25','0.50','0.75',
           '1.00', '1.50','2.00', '2.50','3.00','4.00','5.00').pack()
inputs['LotSize'] = LotSizeVar

#Spread Var SetUp
SpreadVar = StringVar()
SpreadVar.set('Spread Modeling Technique')
OptionMenu(root, SpreadVar, 'Average Spreads').pack()
inputs['Spread'] = SpreadVar

#Trade Management SetUp
TradeManagVar = StringVar()
TradeManagVar.set('Trade Management Technique')
OptionMenu(root,TradeManagVar,'1) Take Profit Stop-Loss', '2) Price % Stop-Loss').pack()
inputs['TradeManag'] = TradeManagVar

#Trade Management SubOptions SetUp
#Trade Management SubOption #1 SetUp
"""TrailingLabel = Label(root,text ='Since " 1) Trailing High/Low Stop-Loss "\
Is\
 Selected,\nEnter Number Of Bars To Trail.')
TrailingLabel.pack()
TrailingEntry = Entry(root, bd = 15)
TrailingEntry.pack()
TrailingLabel.pack_forget()
TrailingEntry.pack_forget()"""
#Trade Management SubOption #1 SetUp
#Take Profit
TakeProfitLabel = Label(root, text = 'Since " 1) Take Profit Stop-Loss " Is \
Selected,\nEnter Take Profit (Number of Pips).')
TakeProfitLabel.pack()
TakeProfitEntry = Entry(root, bd = 15)
TakeProfitEntry.pack()
TakeProfitEntry.config(state = 'normal')
TakeProfitLabel.pack_forget()
TakeProfitEntry.pack_forget()
#Stop Loss
StopLossLabel = Label(root, text ='Since " 1) Take Profit Stop-Loss " Is \
Selected,\
\nEnter Stop-Loss (Number of Pips).')
StopLossLabel.pack()
StopLossEntry = Entry(root, bd = 15)
StopLossEntry.pack()
StopLossLabel.pack_forget()
StopLossEntry.pack_forget()
#Trade Management SubOption #2 SetUp
PricePercentLabel = Label(root, text ='Since " 2) Price % Stop Loss " Is \
Selected,\
\nEnter % Of Price.')
PricePercentLabel.pack()
PricePercentEntry = Entry(root, bd = 15)
PricePercentEntry.pack()
PricePercentLabel.pack_forget()
PricePercentEntry.pack_forget()

#the main code that functions this entire program!!!
def getInputs():
    #going through all the keys in dictionary called inputs
    for parameter in inputs.keys():
        user_input = inputs[parameter].get()
        if user_input == '': #empty string
            tkMessageBox.showinfo(title = 'Input Error', \
                                  message = '{WrongParameter} Is Empty!'.\
                                  format(WrongParameter = parameter))
            raise ValueError('Nothing inputted!')
        parameters[parameter] = user_input
        #populate dictionary with actual user input
    if validateInputs():
        showLoadingBox()
        filename = parameters['Symbol'] + '.csv'
        timeframe1chart = Chart(1)
        timeframe1parser = Parser(filename, timeframe1chart)
        timeframe1parser.parse(parameters['StartDate'],parameters['EndDate'])
        timeframe1chart = timeframe1parser.getChart()
        timeframeuserchart = timeframe1chart.coerceTo(parameters['TimeFrame'])
        usersimulation = Simulation(parameters, timeframeuserchart)
        usersimulation.runSimulation()
        usersimulation.getClosedOrders()
        usersimulation.getOverallBalance()
        usersimulation.getOverallProfit()
        usersimulation.getOverallEquity()
        #load final results back to user, need another pop up so
        #another instance of Tk is necessary to acccomplish this
        master = Tk()
        master.geometry('1100x800+0+0')
        final_result = ''
        final_result_ibalance = ''
        final_result_iequity= ''
        final_result_obalance= ''
        final_result_oequity = ''
        final_result_oprofit = ''
        final_result_scrollbary = Scrollbar(master,orient = VERTICAL)
        final_result_scrollbarx = Scrollbar(master,orient = HORIZONTAL)
        final_result_scrollbary.pack(side = RIGHT, fill = Y)
        final_result_scrollbarx.pack(side = BOTTOM, fill = X)
        final_result_box = Listbox(master,yscrollcommand = \
                                   final_result_scrollbary.set, width=1800,
                                   height = 1000)
        
        #go through all the orders and add them to be displayed
        for order in usersimulation.getClosedOrders():
            final_result_box.insert(END, order)
            
            #if self.balance < 0: self.balance = 0
            # this is because in the real world
            #most forex brokers often do not allow you to go negative,
            #as they have protection plans installed against this happening
            #However, for this purpose, this program will assume no such
            #negative balance protection plan because this program assumes
            #no broker involved but pure raw historical data testing"""

        #return the initial and final recodings back to user 
        final_result_ibalance += 'Your Initial Balance Was:'+ ' ' + str\
                        (parameters['Deposit']) + ' USD ' +'\n'
        final_result_box.insert(END, final_result_ibalance)
        final_result_iequity += 'Your Initial Equity Was:'+ ' ' + str\
                        (parameters['Deposit'] *\
                         parameters['MaxMargin']) + ' USD ' +'\n'
        final_result_box.insert(END, final_result_iequity)
        final_result_obalance += 'Your Overall Balance Now Is:'+' ' + \
                        usersimulation.getOverallBalance()+' USD '+'\n'
        final_result_box.insert(END, final_result_obalance)
        final_result_oequity += 'Your Overall Equity Now Is:'+ ' ' + \
                        usersimulation.getOverallEquity()+' USD '+'\n'
        final_result_box.insert(END, final_result_oequity)
        final_result_oprofit += 'Your Overall Profit/Loss Is:'+ ' ' + \
                        usersimulation.getOverallProfit() + ' USD ' +'\n'
        final_result_box.insert(END, final_result_oprofit)
        final_result_box.pack(side=LEFT, fill=BOTH)
        final_result_scrollbary.config(command=final_result_box.yview)
        final_result_scrollbarx.config(command=final_result_box.xview)
        master.mainloop()
    
def validateInputs():
    initerrorlist = ""
    othererrorlist = ""
    reminderlist = ""
    no_errors_status = False #initialize
    #check that user selects something for TimeFrame
    if parameters['TimeFrame'] == 'TimeFrame':
        initerrorlist +=('TimeFrame Not Selected!\n')
    else:
        #store as integers so that data can be understood by the backtester
        if parameters['TimeFrame'] == 'M1(1 Minute)':
            parameters['TimeFrame'] = 1
        elif parameters['TimeFrame'] == 'M5(5 Minutes)':
            parameters['TimeFrame'] = 5
        elif parameters['TimeFrame'] == 'M15(15 Minutes)':
            parameters['TimeFrame'] = 15
        elif parameters['TimeFrame'] == 'M30(30 Minutes)':
            parameters['TimeFrame'] = 30
        elif parameters['TimeFrame'] == 'H1(1 Hour)':
            parameters['TimeFrame'] = 60
        elif parameters['TimeFrame'] == 'H4(4 Hours)':
            parameters['TimeFrame'] = 240
        elif parameters['TimeFrame'] == 'D1(1 Day)':
            parameters['TimeFrame'] = 60 * 24
        elif parameters['TimeFrame'] == 'W1(1 Week)':
            parameters['TimeFrame'] = 60 * 24 * 7
    #check that user selects something for Symbol
    if parameters['Symbol'] == 'Symbol':
        initerrorlist += ('Symbol Not Selected!\n')
    #check that user selects something for Spread Modeling Technique
    if parameters['Spread'] == 'Spread Modeling Technique':
        initerrorlist += ('Spread Modeling Technique Not Selected!\n')
    #check that user selects something for Trade Management Technique
    if parameters['TradeManag'] == 'Trade Management Technique':
        initerrorlist += ('Trade Management Technique Not Selected!\n')
    #check that user selects something for Position to Trade
    if parameters['Position'] == 'Position To Trade':
        initerrorlist += ('Position To Trade Not Selected!\n')
    #check that user selects something for Trading Criterium
    if parameters['TradingCriterium'] == 'Trading Criterium':
        initerrorlist += ('Trading Criterium Not Selected!\n')
    #check that user selects something for Max Margin
    if parameters['MaxMargin'] == 'Max Margin Ratio':
        initerrorlist += ('Max Margin Not Selected!\n')
    else:
        parameters['MaxMargin'] = int(parameters['MaxMargin'][2:])
    #check that user selects 1something for Lot Size
    if parameters['LotSize'] == 'Preferred Lot Size':
        initerrorlist += ('Preferred Lot Size Not Selected!\n')
    #check that user inputs digits for initial deposit
    if parameters['Deposit'].isdigit() == False:
        initerrorlist += ('Initial Deposit Needs To Be An Integer!\n')
    else:
        parameters['Deposit'] = float(parameters['Deposit'])
    
        
    #check that the user input for StartDate is acceptable
    try:
        #if not in proper format, by default ValueError raised
        parameters['StartDate'] = datetime.datetime.strptime(\
            parameters['StartDate'], '%m/%d/%Y')
        #if not in appropriate range, raise TypeError
        #first ValueError case is when the date is too early
        if parameters['StartDate'] < start_date_availability:
            raise TypeError('Start Date Needs To Be At or After {0}\n'.format\
                            (start_date_availability.strftime('%m/%d/%Y')))
        #second ValueError case is when the date is too late
        if parameters['StartDate'] > end_date_availability:
            raise TypeError('Start Date Needs To Be Before {0}\n'.format(\
            end_date_availability.strftime('%m/%d/%Y')))
                                           
    except ValueError:
        initerrorlist +=('Start Date Is In Invalid Format!\n')
    except TypeError as e:
        initerrorlist += e.__str__()
        #depending on which TypeError is raised, add that string
                                           
    #check that the user input for EndDate is acceptable
    try:
        #if not in proper format, by default ValueError raised
        parameters['EndDate'] = datetime.datetime.strptime(\
            parameters['EndDate'], '%m/%d/%Y')
        #if not in appropriate range, raise TypeError
        #first ValueError case is when the date is too early
        if parameters['EndDate'] < start_date_availability:
            raise TypeError('End Date Needs To Be After {0}\n'.format(\
            start_date_availability.strftime('%m/%d/%Y')))
        #second ValueError case is when the date is too late
        if parameters['EndDate'] > end_date_availability:
            raise TypeError('End Date Needs To Be At or Before {0}\n'.format(\
            end_date_availability.strftime('%m/%d/%Y')))
                                           
    except ValueError:
        initerrorlist += ('End Date Is In Invalid Format!\n')
    except TypeError as e:
        initerrorlist += e.__str__()
        
    #check that user input for StartDate is earlier than EndDate
    if type(parameters['StartDate']) != type(str) and \
            type(parameters['EndDate']) != type(str) and \
            parameters['StartDate'] >= parameters['EndDate']:
        #converted to datetime object so these are built in comparators
        initerrorlist += ('Set Start Date To Be Earlier Than End Date!\n')

    #check it there are any errors, if so display in another box which ones.                             
    if (len(initerrorlist) != 0):
        tkMessageBox.showinfo(title = 'Error(s) In Regular Inputs', \
                              message = initerrorlist)
        
    else: # no errors in initerrorlist
        #elif parameters['TradeManag'] == '1) Take Profit Stop-Loss':
        #else: # parameters['TradeManag'] == '2) Price % Stop-Loss':
        if parameters['TradeManag'] == '1) Take Profit Stop-Loss':
            TakeProfitLabel.pack()
            TakeProfitEntry.pack()
            StopLossLabel.pack()
            StopLossEntry.pack()
            takeprofitvalue = TakeProfitEntry.get()
            parameters['TakeProfit'] = takeprofitvalue
            stoplossvalue = StopLossEntry.get()
            parameters['StopLoss'] = stoplossvalue
            #error handling for take profit
            try:
                if parameters['TakeProfit'].isdigit() == False and \
                   (len(parameters['TakeProfit']) != 0):
                    raise ValueError('Take Profit Value Needs To Be \
An Integer!\n')
                elif parameters['TakeProfit'] <= 0 and \
                     (len(parameters['TakeProfit'])!= 0):
                    raise ValueError('Take Profit Value Needs To \
Be Greater Than Zero!\n')
                elif len(parameters['TakeProfit'] == 0):
                    raise TypeError('Remember, TakeProfit Is Needed!')
            except ValueError as e:
                othererrorlist += e.__str__()
            except TypeError as f:
                reminderlist += f.__str__()
            #error handling for stop loss
            try:
                if parameters['StopLoss'].isdigit() == False and \
                   (len(parameters['StopLoss'])!= 0):
                    raise ValueError('Stop Loss Value Needs To Be \
An Integer!\n')
                elif parameters['StopLoss'] <= 0 and (len(parameters['StopLoss'])!= 0):
                    raise ValueError('Stop Loss Value Needs To \
Be Greater Than Zero!\n')
                elif len(parameters['StopLoss'] == 0):
                    raise TypeError('Remember, Stop Loss Value Is Needed!')
            except ValueError as e:
                othererrorlist += e.__str__()
            except TypeError as f:
                reminderlist += f.__str__()
            #check if othererrorlist msg needs to be displayed
            if len(othererrorlist) != 0 and \
               len(parameters['TakeProfit']) != 0:
                tkMessageBox.showinfo(title = 'Error(s) In Trade \
Management SubOptions', \
                                  message = othererrorlist)
            elif len(othererrorlist) == 0 and \
                 len(parameters['TakeProfit']) != 0 and \
                                       len(parameters['StopLoss']) != 0:
                tkMessageBox.showinfo(title = 'Confirmation Status', \
                                  message = 'Press Ok, and Your Inputs Will \
Be Submitted and Simulated!')
                no_errors_status = True
                return no_errors_status
            
        else: #parameters['TradeManag'] == '2) Price % Stop-Loss'
            PricePercentLabel.pack()
            PricePercentEntry.pack()
            suboption = True
            pricepercentvalue = PricePercentEntry.get()
            parameters['PricePercent'] = pricepercentvalue
            #error handling for Price Percent
            try:
                
                if parameters['PricePercent'].isdigit() == False and \
                   (len(parameters['PricePercent'])!= 0):
                    raise ValueError('Price % Needs To Be A Whole Number!\n')
                elif parameters['PricePercent'] <= 0 and \
                     (len(parameters['PricePercent'])!= 0):
                    raise ValueError('Price % Needs To Be Greater Than Zero!\n')
                elif len(parameters['PricePercent'] == 0):
                    raise TypeError('Remember, Price Percent Value Is Needed!')
            except ValueError as e:
                othererrorlist += e.__str__()
            except TypeError as f:
                reminderlist += f.__str__()
            #check if othererrorlist msg needs to be displayed
            if len(othererrorlist) != 0 and \
               len(parameters['PricePercent']) != 0:
                tkMessageBox.showinfo(title = 'Error(s) In Trade Management \
SubOptions', message = othererrorlist)
            elif len(othererrorlist) == 0 and \
                 len(parameters['PricePercent'])!= 0:
                tkMessageBox.showinfo(title = 'Confirmation Status', \
                                  message = 'Press Ok, and Your Inputs Will \
Be Submitted and Simulated!')
                no_errors_status = True
                return no_errors_status
            
def showLoadingBox():
    tkMessageBox.showinfo(title = 'Testing Status', \
                          message = 'Currently Testing, \
Please Close This Box To Continue Testing.')
            

submit = Button(root, text = "Submit", command = getInputs)
submit.pack(side = BOTTOM)
root.mainloop()
