import copy
from chart_class import *
from moving_average_class import *
from collections import deque
class StochasticOscillatorStrategy(object):
    def __init__(self):pass
    """Stochastic Oscillator is a powerful momentum indicator which takes
    the closing price and compares it to the overall price range to the
    specified time period.
    
    %K is a formula that in a 15 bar period, takes the Low and High of the
    previous 14 bars before it and puts it into a formula:
    
    %K = [(last close of 15th bar)-(Low of previous 14 bars)/
           High of previous 14 bars)] * 100
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
        
    def calculatePercentK(self, newchart, period = 15):
        percentK_list = []
        high_of_14_list = []
        low_of_14_list = []
        org_newchart = copy.deepcopy(newchart)
        newchartdeque = collections.deque(newchart)
        for i in xrange(len(newchart)/period): #number of iterations
            max_high_value = newchartdeque[0].getHighValue()
            min_low_value = newchartdeque[0].getLowValue()
            for eachbar in (period-1): #period-1 b/c last bar not calculated
                if newchartdeque[0].getHighValue() > max_high_value:
                    max_high_value = newchartdeque[0].getHighValue()
                if newchartdeque[0].getLowValue() < min_low_value:
                    min_low_value = newchartdeque[0].getLowValue()
                newchartdeque.popleft()
            #get inputs for calculating K
            high_of_14_list += max_high_value
            low_of_14_list += min_low_value
            #calculate K
            calculate_percentK = \
                       ((newchartdeque[0].getCloseValue())-low_of_14_list[i])/(\
                           high_of_14_list[i]))*100
            percentK_list += calculate_percentK
            #continue throughout all iterations until complete
        return percentK_list

    def calculatePercentD(self, percentK_list, period = 3)
        percentD_list = []
        for i in xrange(0:len(percentK_list): period):
            percentD_list += calculateMovingAverage(percentK_list, period = 3)
        return percentD_list
        
    
