import copy
from collections import deque
from bar_class import Bar
class Chart(object):
    def __init__(self, TimeFrame):
        self._TimeFrame = TimeFrame
        self._ListOfBars = []
    def addBar(self, bar):
         #Bar.getTimeFrame(bar) is also valid instead of bar.getTimeFrame()
        if self._TimeFrame != bar.getTimeFrame():
            raise ValueError
        if type(bar) != Bar:
            raise TypeError
        self._ListOfBars.append(bar)
    def reset(self):
        self._ListOfBars = []
    def isEmpty(self):
        if self._ListOfBars == []:
            return True
        return False
    def __len__(self):
        return len(self._ListOfBars)
    def getBarsList(self):
        return self._ListOfBars
    def getCloseValuesList(self):
        closevalueslist = []
        for eachbar in self._ListOfBars:
            closevalueslist.append(eachbar.getCloseValue())
        return closevalueslist
    """the purpose of the coerceTo function is that since our internal data
    is represented in 1M (every minute) bars, the user input may be
    something that is greater.  If it is greater, the data bars need to
    change so that a new graph corresponding to that data can be represented."""
    
    def coerceTo(self, newtimeframe):
        if newtimeframe == self._TimeFrame:
            return self
        elif newtimeframe < self._TimeFrame:
            raise ValueError('The TimeFrame That You Coerce To Cannot Be \
Smaller!')
        #new chart that coerced bars will be added to
        newchart = Chart(newtimeframe)
        #the width of the new bars of the new chart
        newbarwidth = int(newtimeframe/self._TimeFrame)
        #store the old list just in case
        oldbarslist = copy.deepcopy(self._ListOfBars)
        #creates a deque object that represents a queue of the oldbarslist
        #deque object is for efficient memory management, since we will use
        #'pop' method a lot.
        oldbarsdeque = deque(oldbarslist)
        #the nested for loop is for each section of old bars which comprise
        #one new bar
        #the first for loop is for each new bar
        for _ in xrange(len(self._ListOfBars)/ newbarwidth):
            section = []
            #the number of iterations of this loop is how many old bars are
            #in one new bar
            for _ in xrange(newbarwidth):
                #populate the section, removes and returns the element on
                #the left side of the deque
                section.append(oldbarsdeque.popleft())
            O = section[0].getOpenValue()#does not change
            Close = section[-1].getCloseValue() #does not change
            Date = section[0].getDate() #does not change
            #figure out the highest and lowest 
            maxHighValue = section[0].getHighValue() #initialize
            minLowValue = section[0].getLowValue()  #initialize
            for eachbar in section:
                if eachbar.getHighValue() > maxHighValue:
                    maxHighValue = eachbar.getHighValue()
                if eachbar.getLowValue() < minLowValue:
                    minLowValue = eachbar.getLowValue()
            #create the new bar
            bar = Bar(O,maxHighValue, minLowValue, Close, Date, newtimeframe)
            #add the new bar to the new chart
            newchart.addBar(bar)
        return newchart
            
            
            
            
            
        
            
