import csv
import datetime
from Tkinter import *
import tkMessageBox
from bar_class import *
from chart_class import *

class Parser(object):
    def __init__(self, filename, chart):
        self.filename = filename
        self.chart = chart
    def parse(self,StartDate, EndDate):
        self.chart.reset() #clear chart
        try:
            #open the selected file for reading in binary mode
            ofile = open(self.filename, 'rb')
            reader = csv.reader(ofile)
            firstrow = True
            for row in reader: #look through each row
                if firstrow == True:
                    firstrow = False
                    continue #skip the first 
                spliced_date = row[0][0:(len(row[0])-7)] #get rid of seconds
                date = datetime.datetime.strptime(spliced_date,\
                                                  '%d.%m.%Y %H:%M')
                if StartDate<= date <=EndDate: #found right date
                    O = row[1]
                    H = row[2]
                    L = row[3]
                    C = row[4]
                    Date = date
                    TimeFrame = 1 #1 minute 
                    #create bar object with the variables above
                    bar = Bar(O,H,L,C,Date,TimeFrame)
                    #this bar represents the specific row
                    self.chart.addBar(bar)
                if date > EndDate:
                    break
            
        except IOError:
             tkMessageBox.showinfo(title = 'File Opening Error', \
                                   message = 'Could Not Find Designated Data')
             raise RuntimeError('Fatal Error! Historical Data Cannot Be Read!')
    def getChart(self):
        if self.chart.isEmpty():
            raise RuntimeError('Chart Is Not Parsed With Populated Data!')
        else:
            return self.chart
