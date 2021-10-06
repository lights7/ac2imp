import sys,os
import wx
from wx import xrc
import wx.grid as grd
import re

def export ( path, mapping, grid):
    """
        path: path to save the file
        mapping: mapping selected from mappings.py
        grid: grid with csv data from report_utils.py
    """
    type_tran = "Empty"
    from_or_to="from"
    debt={}
    cred={}
    out=open(path,'w')
    if list(filter(lambda x: 'Checking Account' in x,grid.grid_contents[0])) != []:
        type_tran = "Spend"
        out.write('Checking Account,Date,Co./Last Name,First Name, Memo,Allocation Account #,Amount,Currency Code, Exchange Rate')
    elif list(filter(lambda x: 'Deposit Account' in x,grid.grid_contents[0])) != []:
        type_tran = "Receive"
        out.write('Deposit Account,Date,Co./Last Name,First Name,Memo,Allocation Account #,Amount,Exchange Rate,Currency Code,Payment Method,Check Number,Notes')
    elif type_tran == "Empty":
        print("Warning, Transaction is neither Spend nor Receive")
    for row in range(grid.GetNumberRows()):
        if row > 0:
           if type_tran == "Spend":
              debt=dict([(k,mapping[k](row,grid)) for k in ['FromAcc','Date','lname','fname', 'Memo','ToAcc','Amount', 'ExRate']])
              debt['lname']=debt['lname'].strip() #remove space
              debt['fname']=debt['fname'].strip() #remove space
              debt['Memo']=re.sub(' +',' ',"".join(re.findall("[^\u05C0-\u2100\u214F-\uFFFF]+", debt['Memo']))) # remove Chinese characters

              if float(debt['ExRate']) < 1: 
                  debt['Currency']= "RMB"
                  cred['Currency']= "RMB"
              elif float(debt['ExRate']) == 1:  
                  debt['Currency']= "USD"
                  cred['Currency']= "USD"
              if debt['FromAcc'].replace(' ','')== "":
                  from_or_to="to"
                  cred=debt.copy()    
                  out.write (
                   """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s """ %cred)
                  if row<grid.grid_rows-1 and mapping['FromAcc'](row+1,grid).replace(' ','') != "":
                     out.write ("\n")
              else:
                  from_or_to="from"
                  cred=debt.copy()
                  out.write (
                   """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s""" %debt)
# if From followed by a To, don't write To here, wait next line
                  if row<grid.grid_rows-1 and mapping['FromAcc'](row+1,grid).replace(' ','') != "":
                     out.write (
                   """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s
                   """ %cred)
                  elif row==grid.grid_rows-1:# write for last line
                     out.write (
                   """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s
                   """ %cred)

           elif type_tran == "Receive": # following code are for Receive
              debt=dict([(k,mapping[k](row,grid)) for k in ['DepoAcc','Date','lname','fname','Memo','ToAcc','Amount','ExRate','PayMethod','CheckN']])
              debt['Notes']=debt['CheckN'] #remove space
              debt['lname']=debt['lname'].strip() #remove space
              debt['fname']=debt['fname'].strip() #remove space
              if debt['Memo'].replace(" ","") == "": # if no meno use first and last name as memo
                  debt['Memo']="%s %s" % (mapping['lname'](row,grid), mapping['fname'](row,grid))
#              debt['Memo']=re.sub(' +',' ',"".join(re.findall("[^\u05C0-\u2100\u214F-\uFFFF]+", debt['Memo']))) # remove Chinese characters

              if float(debt['ExRate']) < 1: 
                  debt['Currency']= "RMB"
                  cred['Currency']= "RMB"
              elif float(debt['ExRate']) == 1:  
                  debt['Currency']= "USD"
                  cred['Currency']= "USD"
              if debt['DepoAcc'].replace(' ','')== "":
                  from_or_to="to"
                  cred=debt.copy()    
                  out.write (
                   """
%(DepoAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s,%(Amount)s,%(Currency)s,%(ExRate)s,%(PayMethod)s,%(Notes)s """ %cred)
                  if row<grid.grid_rows-1 and mapping['DepoAcc'](row+1,grid).replace(' ','') != "":
                     out.write ("\n")
              else:
                  from_or_to="from"
                  cred=debt.copy()
                  debt['ToAcc']= "" 
                  cred['Co./Last Name']= "" 
                  cred['Co./Last Name']= "" 
                  cred['FromAcc']= "" 
                  out.write (
                   """
%(DepoAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s,%(Amount)s,%(Currency)s,%(ExRate)s,%(PayMethod)s,%(Notes)s """ %debt)
#%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(Exchange Rate)s""" %debt)
# if From followed by a To, don't write To here, wait next line
                  if row<grid.grid_rows-1 and mapping['DepoAcc'](row+1,grid).replace(' ','') != "":
                     out.write (
                   """
%(DepoAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s,%(Amount)s,%(Currency)s,%(ExRate)s,%(PayMethod)s,%(Notes)s
""" %cred)
                  elif row==grid.grid_rows-1:# write for last line
                     out.write (
                   """
%(DepoAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s,%(Amount)s,%(Currency)s,%(ExRate)s,%(PayMethod)s,%(Notes)
""" %cred)

              
    return 0

