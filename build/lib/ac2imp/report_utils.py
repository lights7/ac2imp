

from datetime import datetime
import csv 
#from wx.grid import PyGridTableBase
import wx.grid as grd

class Accounting(grd.GridTableBase):
    """
        A very basic instance that allows the bank register of AccountEge contents to be used in a wx.Grid
        make sure the bank register report include the name of the
        organization(company), Company Address, Report Date and Time.
        This should be default, 
    """

    def __init__(self,csv_path,delimiter=',',skip_last=0):

        grd.GridTableBase.__init__(self)
          # delimiter, quote could come from config file perhaps
        csv_reader = csv.reader(open(csv_path,'r'),delimiter=delimiter,quotechar='"')
        print("report1\n")
        self.grid_contents = [row for row in csv_reader if len(row)>1]
        print("report2\n")
#        company_name = self.grid_contents[0]
#        company_street = self.grid_contents[1]
#        company_city = self.grid_contents[2]
#        self.report_name = self.grid_contents[3][0] # Should be Bank Register 
           
#        if list(filter(lambda x: 'Checking Account' in x,self.grid_contents[0])) != []:
#            type_tran = "Spend"
#        if list(filter(lambda x: 'Deposit Account' in x,self.grid_contents[0])) != []:
#            type_tran = "Receive"
#        self.report_period = self.grid_contents[4] 
#        report_date = self.grid_contents[5] 
#        report_time = self.grid_contents[6] 
#        if self.grid_contents[1].str.contains("Checking Account"):

        self.grid_colnum = []
        self.payment_method={}
        self.check_number={}

        if skip_last:
            self.grid_contents=self.grid_contents[0:-skip_last]
        
        self.grid_rows = len(self.grid_contents)
        self.grid_cols = len(self.grid_contents[0])
#        print("rows, cols", self.grid_rows, self.grid_cols)
       # the 1st row is the column headers
        for I in range (self.grid_rows):

           if len(self.grid_contents[I])>=8: # check if the line if empty
               self.grid_colnum.append(len(self.grid_contents[I])) # setup the colnum of row I
           else:
               print("At line",I)
               print("input date length is less than 8, only has",len(self.grid_contents[I])) # check if the line if empty
               exit 
#           if len(self.grid_contents[I])>8: # check if there is column for payment method
#               self.payment_method[self.grid_contents[I][1]] = self.grid_contents[I][8]
#           elif len(self.grid_contents[I])>1:
#               self.payment_method[self.grid_contents[I][1]] = ' '

#           print("report3\n")
#           if len(self.grid_contents[I])>9: # check if there is column for payment method
#               self.check_number[self.grid_contents[I][1]] = self.grid_contents[I][9]
#           elif len(self.grid_contents[I])>1:
#               self.check_number[self.grid_contents[I][1]] = ' '
#           print("report4\n")
        
        # header map
        # results in a dictionary of column labels to numeric column location            
        self.col_map=dict([(self.grid_contents[0][c],c) for c in range(self.grid_cols)])
        
    def GetNumberRows(self):
        return self.grid_rows
    
    def GetNumberCols(self):
        return self.grid_cols
    
    def GetColNum(self,row):
        return self.grid_colnum[row]

    def IsEmptyCell(self,row,col):
#        print(row-1,self.grid_colnum[row-1])
#        print(row-1)
        if col<self.grid_colnum[row]: 
            return len(self.grid_contents[row][col]) == 0 
        else: 
            return 0
    
    def GetValue(self,row,col): 
        if col<self.grid_colnum[row]: 
            return self.grid_contents[row][col] 
        else: 
            return ''
    
    def GetColLabelValue(self,col): return self.grid_contents[1][col]
    
    def GetColPos(self,col_name): return self.col_map[col_name]
    
    def GetPeriod(self): return self.report_period
    
def xmlize(dat): 
    """ Xml data can't contain &,<,> replace with &amp; &lt; &gt; Get newlines while we're at it.  """ 
    return dat.replace('&','and').replace('<','&lt;').replace('>','&gt;').replace('\r\n',' ').replace('\n',' ').replace('?','')
    
def fromCSVCol(row,grid,col_name): 
    """ Uses the current row and the name of the column to look up the value from the csv data.  """ 
    return xmlize(grid.GetValue(row,grid.GetColPos(col_name)))

    
