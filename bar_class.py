import datetime
class Bar(object):
    def __init__(self,O,H,L,C,Date,TimeFrame):
        self._O = float(O) #store the Open value, do not access directly
        self._H = float(H) #store the High value, do not access directly
        self._L = float(L) #store the Low value, do not access directly
        self._C = float(C) #store the Close value, do not access directly
        self._Date = Date #store the Date, do not access directly
        self._TimeFrame = int(TimeFrame)
        #store the TimeFrame as an integer representing in minutes,
        #do not access directly
    def __str__(self):
        return str(self._O) + ',' + str(self._H) + ',' + str(self._L) + ',' +str(self._C)
    def __repr__(self):
        return str(self._O) + ',' + str(self._H) + ',' + str(self._L) + ',' +str(self._C)
    #data abstraction
    def setOpenValue(self,value):
        self._O = value
        return True
    def setHighValue(self,value):
        self._H = value
        return True
    def setLowValue(self,value):
        self._L = value
        return True
    def setCloseValue(self,value):
        self._C = value
        return True
    def getOpenValue(self):
        return self._O
    def getHighValue(self):
        return self._H
    def getLowValue(self):
        return self._L
    def getCloseValue(self):
        return self._C
    def getDate(self):
        return self._Date
    def getTimeFrame(self):
        return self._TimeFrame
    def isInBarBody(self, value):
        #bar body is based upon Open and Close
        #the High and Low Values are the wicks, and are ignored in this case
        if self.isBullish:
            return (self._O <= value <= self._C)
        if self.isBearish:
            return (self._C <= value <= self._O)
    def isInBar(self,value):
        if self.isBullish:
            return (self._L <= value <= self._H)
        if self.isBearish:
            return (self._H <= value <= self._L)
            
            
    @property
    def isBullish(self):
        if self._O < self._C:
            return True
        return False
    @property
    def isBearish(self):
        if self._C < self._O:
            return True
        return False
    @property
    def endTimeOfBar(self):
        return self._Date + datetime.timedelta(0,60*self._TimeFrame)
    #From my historical data which is represented for every minute,
    #timedelta works so that it is (day,seconds,....)
    #therefore, convert each minute into seconds
        
        
