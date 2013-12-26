import copy
from chart_class import *
from moving_average_class import *
from collections import deque
class StochasticOscillatorStrategy(object):
    def moving_average(self,iterable, n=3): \
    # THIS IS FROM PYTHON DEQUE DOCS LIBRARY!!!!
    # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
    # http://en.wikipedia.org/wiki/Moving_average
        it = iter(iterable)
        d = deque(islice(it, n-1))
        d.appendleft(0)
        s = sum(d)
        for elem in it:
            s += elem - d.popleft()
            d.append(elem)
            yield s / float(n)
    def __init__(self,chart):
        self.DEFAULT_PERIOD_K = 15
        self.DEFAULT_PERIOD_D = 3
        self.chart = chart
        self.percentK_list = []
        self.percentD_list = []
        
    """Stochastic Oscillator is a powerful momentum indicator which takes
    the closing price and compares it to the overall price range to the
    specified time period.
    
    %K is a formula that in a 15 bar period, takes the Low and High of the
    previous 14 bars before it and puts it into a formula:
    
    %K = [(last close of 15th bar)-(Low of previous 14 bars)/
           (High of previous 14 bars- Low of previous 14 bars)] * 100
    %D is a formula that represents the 3 period moving average of %K"""
    
    """with given period of 15, this refers to the slow stochastic,
    the slow stochastic is the most commonly used one, while a fast stochastic
    would be like that of a period of 5"""

    
    """To determine when to buy/sell is on the 80/20 line(*80 is known as
    the Overbought line, 20 is known as the Oversold line):
    
    If the %D is over the 80 line AND %K crosses below %D, that is the signal
    to sell.  If %D is below the 20 line (Oversold line) AND %K crosses above
    %D, that is the signal to buy.  Overall, when the currency pair is
    overbought, the program sells(shorts). When the currency pair is oversold,
    the program buys(longs).  The %K and %D crossovers are just additional
    checks upon when is the 'optimal' time to take action.
    Of course, this is determinant upon whether the user input has allowed for
    both long and short option or only one or the other."""
        
    def calculateIndicator(self):
        period = self.DEFAULT_PERIOD_K
        org_newchart = copy.deepcopy(self.chart.getBarsList())
        newchartdeque = deque(self.chart.getBarsList())
        length_of_chart = len(self.chart.getBarsList())
        for i in xrange(period-1,length_of_chart):#starting from the 15th value
            high_of_14 = newchartdeque[i].getHighValue() #initialize
            low_of_14= newchartdeque[i].getLowValue()#initialize 
            for everygroup in xrange(i-period+1,i-1): #check previous 14 values
                if newchartdeque[everygroup].getHighValue() > high_of_14:
                    high_of_14 = newchartdeque[everygroup].getHighValue()
                if newchartdeque[everygroup].getLowValue() < low_of_14:
                    low_of_14 = newchartdeque[everygroup].getLowValue()
            fifteenth_value_close = newchartdeque[i].getCloseValue()#15thvalue
            if high_of_14- low_of_14 == 0:
                calculate_percentK = 100
            else:
                calculate_percentK =100*((fifteenth_value_close - low_of_14)/\
                                      ((high_of_14)-(low_of_14)))
            self.percentK_list.append(calculate_percentK)
        #add the zeros to the beginning of the list so that the two lists can
        #be compared index by index later on                                          
        self.percentK_list = [0]*((self.DEFAULT_PERIOD_K)-1)+self.percentK_list         
        #for i in xrange 0:len(self.percentK_list):self.DEFAULT_PERIOD_D):
        #percentD_list += calculateMovingAverage(percentK_list, period = 3)
        for percentKval in self.moving_average(self.percentK_list,\
                                               self.DEFAULT_PERIOD_D):
                                  self.percentD_list.append(percentKval)
        #add the zeros to the beginning of the list so that the two lists can
        #be compared index by index later on
        self.percentD_list = [0]*((self.DEFAULT_PERIOD_D) -1)+ \
                                  self.percentD_list

    def getBuySignals(self):
        #return indexes that indicate buying opportunities in a list and \
        #return indexes that return selling options in a list
        barlist = self.chart.getBarsList()
        buy_signal_index_list = []
        for index in xrange(len(barlist)-1):
            percentKBarZero = self.percentK_list[index]
            percentKBarOne = self.percentK_list[index+1]
            percentDBarZero = self.percentD_list[index]
            percentDBarOne = self.percentD_list[index+1]
            #the constraints to buy: D is below 20 line and K crosses over D
            if (percentDBarZero <= 20 and percentKBarZero < percentDBarZero and \
                percentKBarOne > percentDBarZero):
                                  buy_signal_index_list.append(int(index+1))
        return buy_signal_index_list
                                  
    def getSellSignals(self):
        #return indexes that indicate buying opportunities in a list and \
        #return indexes that return selling options in a list
        barlist = self.chart.getBarsList()
        length = len(barlist)- 1
        sell_signal_index_list = []
        for index in xrange(length):
            percentKBarZero = self.percentK_list[index]
            percentKBarOne = self.percentK_list[index+1]
            percentDBarZero = self.percentD_list[index]
            percentDBarOne = self.percentD_list[index+1]
            #the constraints to sell: D is above 80 line and K crosses below D
            if (percentDBarZero >= 80 and percentKBarZero > percentDBarZero and \
                percentKBarOne < percentDBarZero):
                                  sell_signal_index_list.append(int(index+1))
        return sell_signal_index_list
        
    
