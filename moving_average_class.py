import copy
from bar_class import *
from chart_class import *
from collections import deque
from itertools import *

"""Moving Average is a standard indicator that smooths out price fluctuation
that simply takes the average of the closing prices for the given period."""
    
class MovingAverageStrategy(object):
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
    def __init__(self, chart):
        self.DEFAULT_SLOW_PERIOD = 30
        self.DEFAULT_FAST_PERIOD = 5
        self.fastMAlist = []
        self.slowMAlist = []
        self.chart = chart
    #to calculate moving average, based upon the period you average the
    #closing prices of the last ___ bars (____ is determined by period)
    def calculateIndicator(self):
        for fastMAValue in self.moving_average(self.chart.getCloseValuesList()\
                                               , self.DEFAULT_FAST_PERIOD):
            self.fastMAlist.append(fastMAValue)
        #you want to pop the values to be 0 where there are gaps
        #so that the indices of both lists match one another when needed
        self.fastMAlist = [0]*((self.DEFAULT_FAST_PERIOD)-1) + self.fastMAlist
        for slowMAValue in self.moving_average(self.chart.getCloseValuesList(),\
                                               self.DEFAULT_SLOW_PERIOD):
            self.slowMAlist.append(slowMAValue)
        self.slowMAlist = [0]*((self.DEFAULT_SLOW_PERIOD)-1) + self.slowMAlist
        #self.slowMAlist = self.moving_average(self.chart.getBarsList(), \
        #self.DEFAULT_SLOW_PERIOD)
        #self.slowMAlist = [0]*((self.DEFAULT_SLOW_PERIOD)-1) +
        #self.slowMAlist

        #I tried to develop my own moving_average code, there was a bug.
        #But I did learn how to utilize generator functions instead.
        """slow_close_list = [] #list of all closes
        fast_close_list = []
        barsdeque = deque(self.chart.getBarsList())
        #number of iterations
        
        for _ in xrange(len(self.chart.getBarsList())/self.DEFAULT_SLOW_PERIOD):
            #every bar within that period
            for eachbar in xrange(self.DEFAULT_SLOW_PERIOD): 
                slow_close_list.append(barsdeque.popleft().getCloseValue())
            self.slowMAlist.append(sum(slow_close_list)/self.DEFAULT_SLOW_PERIOD\
            )
            slow_close_list = []
        self.slowMAlist = [0]*((self.DEFAULT_SLOW_PERIOD)-1) + self.slowMAlist
        #next loop
        barsdeque = deque(self.chart.getBarsList())
        for _ in xrange(len(self.chart.getBarsList())/self.DEFAULT_FAST_PERIOD):
            #every bar within that period
            for eachbar in xrange(self.DEFAULT_FAST_PERIOD): 
                fast_close_list.append(barsdeque[0].getCloseValue())
                barsdeque.popleft()
            self.fastMAlist.append(sum(fast_close_list)/self.DEFAULT_FAST_PERIOD)
            fast_close_list = []
        self.fastMAlist = [0]*((self.DEFAULT_FAST_PERIOD)-1) + self.fastMAlist"""
        
    def getBuySignals(self):
        #return indexes that indicate buying opportunities in a list and \
        #return indexes that return selling options in a list
        barlist = self.chart.getBarsList()
        buy_signal_index_list = []
        for index in xrange(len(barlist)-1):
            fastMABarZero = self.fastMAlist[index]
            fastMABarOne = self.fastMAlist[index+1]
            slowMABarZero = self.slowMAlist[index]
            slowMABarOne = self.slowMAlist[index+1]
            if (slowMABarZero > fastMABarZero and fastMABarOne >slowMABarZero):
                buy_signal_index_list.append(int(index+1))
        return buy_signal_index_list
    
    def getSellSignals(self):
        #return indexes that indicate buying opportunities in a list and \
        #return indexes that return selling options in a list
        barlist = self.chart.getBarsList()
        sell_signal_index_list = []
        for index in xrange(len(barlist)-1):
            fastMABarZero = self.fastMAlist[index]
            fastMABarOne = self.fastMAlist[index+1]
            slowMABarZero = self.slowMAlist[index]
            slowMABarOne = self.slowMAlist[index+1]
            if (fastMABarZero > slowMABarZero and slowMABarOne > \
                fastMABarZero):
                sell_signal_index_list.append(int(index+1))
        return sell_signal_index_list

        """ This was an inefficient and more confusing way that I ditched."
        #buy signal and sell signal list containing crossover points
        #on when to buy or sell
        buy_signal_list = []
        sell_signal_list = []
        #list of what type of order is occuring for each bar
        buy_order_range_list = [] 
        sell_order_range_list = []
        #for maximized data structure optimization and efficient
        #memory management for upcoming actions
        FastMAdeque = deque(FastMA)
        SlowMAdeque = deque(SlowMA)
        #store the old lists for comparison purposes
        OrgFastMAList = copy.deepcopy(FastMA)
        OrgSlowMAList = copy.deepcopy(SlowMA)
        #compare the leftmost element always with each other
        signal = FastMAdeque[0] - SlowMAdeque[0]
        #for loop goes through each bar
        for eachbar in len(FastMAdeque):
            if signal > 0:
                #to check that a sell order was placed previously
                if buy_signal_list != []:
                    buy_order_range_list += newchart[eachbar]
                FastMAdeque.popleft()
                SlowMAdeque.popleft()
            elif signal < 0:
                if sell_signal_list != []:
                    sell_order_range_list += newchart[eachbar]
                FastMAdeque.popleft()
                SlowMAdeque.popleft()
            else:
                while signal == 0: #crossover occurs at that point
                #determine if next bar becomes a buy or sell signal
                    previousbar = 0
                    determine_signal = OrgFastMAList[previousbar+1] - \
                               OrgSlowMAList[previousbar+1]
                    FastMAdeque.popleft()
                    SlowMAdeque.popleft()
                    if determine_signal > 0: 
                        buy_signal_list += FastMAdeque[0]
                        break
                    elif determine_signal < 0:
                        sell_signal_list += SlowMAdeque[0]
                        break
                    else: #equal again, compare next bar
                        previousbar += 1"""
        
        
            
