
# mapping tells the next functions where to get the data for each row
# each key in a mapping must return a function that takes
# the current row and the SimpleCSVGrid object
# the function must return the OFX data for that field.

# NOTE I thought about simply having a dicionary from key fields to column numbers
# but that was not flexible enough to combine column data dynamically
# in order to get custom data from the CSV file.
# (example Memo/Description/BankID/Account id in the yodlee data)

"""
    Mappings API.

    report_utils provides the functions fromCSVCol,xmlize and the grid that holds the csv data.
    fromCSVCol(row,grid,column)
        row: the row number
        grid: the csv data
        column: the case sensitive column header

        returns the csv data for that location

    a mapping is a dictionary of functions.  The exporters call the function for each key
    in the dictionary.  You are free to use any functions or custom logic to return whatever
    data you prefer so that you get the correct data in the fields required by the export format.
    The format of the function that must be returned is:

    def custfunc(row,grid)

    If you have a one-to-one mapping for a key to the CSV data, you can easily just use fromCSVCol.

    Example:

    'CHECKNUM':lambda row,grid: fromCSVCol(row,grid,'Check Number')

    Special parameters for import use these keys:

        delimiters: delimiter for CSV, default to ','
        skip_last: number of lines to skip at the end of the CSV file, default to 0

"""

from .report_utils import *
#left side is in program and convert to, right side is in input file and convert from
AccountEdge = {
#Checking Account,Date,Co./Last Name,Memo,Allocation Account #,Amount,Currency Code, Exchange Rate
    'AccountEdge':{
#        'skip':lambda row,grid: fromCSVCol(row,grid,'Customer') == 'Donor',
        'ChecAcc':lambda row,grid: fromCSVCol(row,grid,'Checking Account'), 
        'DepoAcc':lambda row,grid: fromCSVCol(row,grid,'Deposit Account'), 
#        'Name':lambda row,grid: toOFXDate(fromCSVCol(row,grid,'Date')),
        'Date':lambda row,grid: fromCSVCol(row,grid,'Date'),
        'Memo':lambda row,grid: fromCSVCol(row,grid,'Memo'),
        'lname':lambda row,grid: fromCSVCol(row,grid,'Co./Last Name'), 
        'fname':lambda row,grid: fromCSVCol(row,grid,'First Name'), 
        'ToAcc':lambda row,grid: fromCSVCol(row,grid,'Allocation Account #'), 
        'Amount':lambda row,grid: fromCSVCol(row,grid,'Amount'),
        'ExRate':lambda row,grid: fromCSVCol(row,grid,'Exchange Rate'),
        'Currency':lambda row,grid: fromCSVCol(row,grid,'Currency Code'),
        'CheckN':lambda row,grid: fromCSVCol(row,grid,'Check Number'),
        'Notes':lambda row,grid: fromCSVCol(row,grid,'Notes'),
        'PayMethod':lambda row,grid: fromCSVCol(row,grid,'Payment Method'),
        'Debit':lambda row,grid: fromCSVCol(row,grid,'Debit'),
        'Credit':lambda row,grid: fromCSVCol(row,grid,'Credit'),
#        'Payment Method':lambda row,grid: payment_method(fromCSVCol(row,grid,'ID#')),
#        'Check No.':lambda row,grid: check_number(fromCSVCol(row,grid,'ID#'')),
#Checking Account,Date,Co./Last Name,Memo,Allocation Account #,Amount,Currency Code, Exchange Rate
#Deposit Account,Date,Co./Last Name,First Name,Memo,Allocation Account #,Amount,Exchange Rate,Currency Code,Check Number,Notes

    },
}

all_mappings = {'AccountEdge':AccountEdge}
