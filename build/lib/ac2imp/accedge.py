import sys,os
import wx
from wx import xrc
import wx.grid as grd
import re

def export (path_receive, path_spend, mapping, grid):
    """
        path: path to save the file
        mapping: mapping selected from mappings.py
        grid: grid with csv data from report_utils.py
    """
    type_tran = "Empty"
    from_or_to="from"
    left=0.00
    data={}
    depo={}
    out_receive=open(path_receive,'w')
    out_spend=open(path_spend,'w')
    account_type=list(filter(lambda x: 'Checking Account' in x,grid.grid_contents[0])) 
#    amount_sign=list(filter(lambda x: 'Amount' in x,grid.grid_contents[0])) 
    out_spend.write('Checking Account,Date,Co./Last Name,First Name, Memo,Allocation Account #,Amount,Currency Code, Exchange Rate')
    out_receive.write('Deposit Account,Date,Co./Last Name,First Name,Memo,Allocation Account #,Amount,Currency Code,Exchange Rate,Payment Method,Check Number,Notes')
    if list(filter(lambda x: 'Account' in x,grid.grid_contents[0])) == []: 
        print("Error, first row need to be collum title")
        return 20
    if account_type!= []:
        type_tran = "Spend"
    elif list(filter(lambda x: 'Deposit Account' in x,grid.grid_contents[0])) != []:
        type_tran = "Receive"
    elif type_tran == "Empty":
        print("Warning, Transaction is neither Spend nor Receive")
    for row in range(grid.GetNumberRows()):
        if row > 0 :
#           if type_tran == "Spend" and float(mapping['Amount'](row,grid).replace("RMB","").replace("$","").replace("USD","")) > 0:
           date=grid.GetValue(row,1).strip()
           temp = date.split("/") 
           if int(temp[0]) >12:
               date=temp[1]+'/'+temp[2]+'/'+temp[0]
           if type_tran == "Spend":
               data=dict([(k,mapping[k](row,grid)) for k in ['Date','lname','fname', 'Memo','ToAcc','Amount', 'ExRate']])
               data['FromAcc']=grid.GetValue(row,0).strip()
               data['Amount']=float(data['Amount'].replace("RMB","").replace("$","").replace("USD","")) 
               toacc=data['ToAcc'].replace(" ","") 
               data['Date']=date
               if toacc != "" and toacc[0] == '4': #Receive in Spend
                   tran = "Receive in Spend"
#                   data['Amount']=data['Amount']
                   data['PayMethod']="Online Transfer"
#                   paymethod=grid.grid_contents(row)(8)
                   data['CheckN']=""
                   data['Notes']=data['CheckN'] # for Receive
               else:
                   tran = "Spend in Spend"
                   if data['Amount'] < 0 and toacc[0] !='6' :
                      data['ToAcc'] = data['FromAcc']
                      data['FromAcc'] = toacc
                      data['Amount'] = 0.0 - data['Amount']
           elif type_tran == "Receive":
               data=dict([(k,mapping[k](row,grid)) for k in ['Date','lname','fname', 'Memo','ToAcc','Amount', 'ExRate', 'PayMethod','CheckN']])
               data['FromAcc']=grid.GetValue(row,0).strip()
               data['Notes']=data['CheckN'] # for Receive
               data['Amount']=float(data['Amount'].replace("RMB","").replace("$","").replace("USD","")) 
#               if data['Amount'] < 0:
               toacc=data['ToAcc'].replace(" ","") 
               data['Date']=date
               if toacc != "" and toacc[0] != '4': #Spend in Receive
                   tran = "Spend in Receive"
#                   data['Amount']=0.000-data['Amount']
               else:
                   tran = "Receive in Receive"

           data['lname']=data['lname'].strip() #remove space
           data['fname']=data['fname'].strip() #remove space
           data['Memo']=re.sub(' +',' ',"".join(re.findall("[^\u05C0-\u2100\u214F-\uFFFF]+", data['Memo']))) # remove Chinese characters
# preprocess for Receive money
           if data['Memo'].replace(" ","") == "": # if no meno use first and last name as memo
               data['Memo']="%s %s" % (mapping['lname'](row,grid), mapping['fname'](row,grid))
           if float(data['ExRate']) < 1: 
               data['Currency']= "RMB"
               depo['Currency']= "RMB"
           elif float(data['ExRate']) == 1:  
               data['Currency']= "USD"
               depo['Currency']= "USD"
#           if type_tran == "Spend" and ['Amount'](row,grid).replace("RMB","").replace("$","").replace("USD","")) > 0:
           if data['FromAcc'].replace(' ','')!= "":# new transaction and data
              from_or_to="from"
              if left != 0.0 :
                  print(data)
                  print(depo)
                  print("warning, the balance is not zero")
#              left=float(data['Amount'].replace("RMB","").replace("$","").replace("USD",""))
#              left=data['Amount']
              depo=data.copy()
              spent=depo['Amount']
              if tran == "Spend in Spend" or tran == "Spend in Receive" : # Transaction is spend
                  out_spend.write (
                 """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s""" %data)
# if From followed by a To, don't write To here, wait next line
#                  if row<grid.grid_rows-1 and grid.grid_content(row+1,0).replace(' ','') != "": #if followed a new transaction then write out the current Credit transaction 
                  if row<grid.grid_rows-1 and grid.grid_contents[row+1][0].replace(' ','') != "": #if followed a new transaction then write out the current Credit transaction 
                     left=left-left
                     out_spend.write (
               """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s
               """ %depo)
                  elif row==grid.grid_rows-1:# write for last line
                     left=left-spent
                     out_spend.write (
               """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s
               """ %depo)
              elif tran == "Receive in Receive" or tran == "Receive in Spend" : # Transaction is Receive or Receive in Spend
                  out_receive.write (
                 """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s,%(PayMethod)s,%(CheckN)s,%(Notes)s """ %data)
# if From followed by a To, don't write To here, wait next line
#                  if row<grid.grid_rows-1 and mapping['FromAcc'](row+1,grid).replace(' ','') != "": #if followed a new transaction then write out the current Credit transaction 
                  if row<grid.grid_rows-1 and grid.grid_contents[row+1][0].replace(' ','') != "": #if followed a new transaction then write out the current Credit transaction 
                     left=left-left
                     out_receive.write (
               """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s,%(PayMethod)s,%(CheckN)s,%(Notes)s 
               """ %depo)
                  elif row==grid.grid_rows-1:# write for last line
                     left=left-spent
                     out_receive.write (
               """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s,%(PayMethod)s,%(CheckN)s,%(Notes)s 
               """ %depo)

           else: 

               from_or_to="to"
               depo=data.copy()    
               data['ToAcc']= "" 
               depo['Co./Last Name']= "" 
               depo['First Name']= "" 
               depo['FromAcc']= "" 
               spent=depo['Amount']
#               spent=float(depo['Amount'].replace("RMB","").replace("$","").replace("USD",""))
               left=left-spent

               if type_tran == "Spend" or tran == "Spend in Receive" : # Transaction is spend but in Receive file

                  out_spend.write (
                   """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s """ %depo)
                  if row<grid.grid_rows-1 and grid.grid_contents[row+1][0].replace(' ','') != "": #if followed a new transaction then write out the current Credit transaction 
#                  if row<grid.grid_rows-1 and mapping['FromAcc'](row+1,grid).replace(' ','') != "":
                     out_spend.write ("\n")

               else: # Transaction is Receive

                  out_receive.write (
                   """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s,%(PayMethod)s,%(CheckN)s,%(Notes)s  """ %depo)
                  if row<grid.grid_rows-1 and grid.grid_contents[row+1][0].replace(' ','') != "": #if followed a new transaction then write out the current Credit transaction 
#                  if row<grid.grid_rows-1 and mapping['FromAcc'](row+1,grid).replace(' ','') != "":
                     out_receive.write ("\n")

    out_receive.close()
    out_spend.close()
    return 0



def credit_export (path_receive, path_spend, mapping, grid):
    """
        path: path to save the file
        mapping: mapping selected from mappings.py
        grid: grid with csv data from report_utils.py
    """
    type_tran = "Empty"
    from_or_to="from"
    left=0.00
    data={}
    depo={}
    out_receive=open(path_receive,'w')
    out_spend=open(path_spend,'w')
    account_type=list(filter(lambda x: 'Checking Account' in x,grid.grid_contents[0])) 
#    amount_sign=list(filter(lambda x: 'Amount' in x,grid.grid_contents[0])) 
    out_spend.write('Checking Account,Date,Co./Last Name,First Name, Memo,Allocation Account #,Amount,Currency Code, Exchange Rate')
    out_receive.write('Deposit Account,Date,Co./Last Name,First Name,Memo,Allocation Account #,Amount,Currency Code,Exchange Rate,Payment Method,Check Number,Notes')
    if account_type!= []:
        type_tran = "Spend"
    elif list(filter(lambda x: 'Deposit Account' in x,grid.grid_contents[0])) != []:
        type_tran = "Receive"
    elif type_tran == "Empty":
        print("Warning, Transaction is neither Spend nor Receive")
    for row in range(grid.GetNumberRows()):
        if row > 0 :
           first_acc=grid.GetValue(row,0).strip()
           if first_acc != "":
              first_lett=first_acc[0]
           data['FromAcc']=first_acc
#           data['FromAcc']=grid.GetValue(row,0).strip()
#           if type_tran == "Spend" and float(mapping['Amount'](row,grid).replace("RMB","").replace("$","").replace("USD","")) > 0:
           if type_tran == "Spend":
               data=dict([(k,mapping[k](row,grid)) for k in
                   ['Date','lname','fname', 'Memo','ToAcc','Debit','Credit', 'ExRate']])
               toacc=data['ToAcc'].strip()
               if first_acc.replace(" ","") == "" or toacc=="":
                   print("Account information cannot be empty for Credit transaction")
                   print(data)
                   return 15
               if data['Credit'].replace(" ","") != "" and toacc[0] == "6" : #Credit
                   tran = "Spend in Spend"
                   first_acc=grid.GetValue(row,0).strip()
                   data['FromAcc']=first_acc
                   data['Amount']=float(data['Credit'].replace("RMB","").replace("$","").replace("USD","")) 
                   data['Amount']=0.0-data['Amount']
               elif data['Credit'].replace(" ","") != "" and toacc[0] == "4" : #Credit Deposit
                   tran = "Receive in Spend"
                   first_acc=grid.GetValue(row,0).strip()
                   data['FromAcc']=first_acc
#                   data['ToAcc']=
                   data['Amount']=float(data['Credit'].replace("RMB","").replace("$","").replace("USD","")) 
#                  data['Amount']=data['Amount']
                   data['PayMethod']="Online Transfer"
#                   paymethod=grid.grid_contents(row)(8)
                   data['CheckN']=""
                   data['Notes']=data['CheckN'] # for Receive
               elif data['Credit'].replace(" ","") == "" and toacc[0] == "6" : #Debit
                   tran = "Spend in Spend"
                   data['FromAcc']=first_acc
                   data['Amount']=abs(float(data['Debit'].replace("RMB","").replace("$","").replace("USD","")))
               else :
                   tran = "Spend in Spend"
                   data['FromAcc']=data['ToAcc']
                   data['ToAcc']= first_acc
                   data['Amount']=abs(float(data['Debit'].replace("RMB","").replace("$","").replace("USD","")))

           elif type_tran == "Receive":
               data=dict([(k,mapping[k](row,grid)) for k in
                   ['Date','lname','fname', 'Memo','ToAcc','Debit','Credit', 'ExRate', 'PayMethod','CheckN']])
               data['Notes']=data['CheckN'] # for Receive
               data['Amount']=float(data['Amount'].replace("RMB","").replace("$","").replace("USD","")) 
               if data['Credit'].replace(" ","") != "":#Credit
                   data['FromAcc']=data['ToAcc']
                   data['ToAcc']= first_acc
                   if first_acc.replace(" ","") == "":
                       print("Checking Account cannot be empty for Credit transaction")
                       print(data)
                       exit(15)
                   data['Amount']=float(data['Credit'].replace("RMB","").replace("$","").replace("USD","")) 
               else:
                   first_acc=grid.GetValue(row,0).strip()
                   data['FromAcc']=first_acc
                   data['Amount']=float(data['Debit'].replace("RMB","").replace("$","").replace("USD","")) 
               toacc=data['ToAcc'].replace(" ","") 
               if toacc != "" and toacc != '4': #Spend in Receive
                   tran = "Spend in Receive"
#                   data['Amount']=0.000-data['Amount']
               else:
                   tran = "Receive in Receive"

           data['lname']=data['lname'].strip() #remove space
           data['fname']=data['fname'].strip() #remove space
           data['Memo']=re.sub(' +',' ',"".join(re.findall("[^\u05C0-\u2100\u214F-\uFFFF]+", data['Memo']))) # remove Chinese characters
# preprocess for Receive money
           if data['Memo'].replace(" ","") == "": # if no meno use first and last name as memo
               data['Memo']="%s %s" % (mapping['lname'](row,grid), mapping['fname'](row,grid))
           if float(data['ExRate']) < 1: 
               data['Currency']= "RMB"
               depo['Currency']= "RMB"
           elif float(data['ExRate']) == 1:  
               data['Currency']= "USD"
               depo['Currency']= "USD"
#           if type_tran == "Spend" and ['Amount'](row,grid).replace("RMB","").replace("$","").replace("USD","")) > 0:

           if data['FromAcc'].replace(' ','')!= "":# new transaction and data
              from_or_to="from"
              if left != 0.0 :
                  print(data)
                  print(depo)
                  print("warning, the balance is not zero")
#              left=float(data['Amount'].replace("RMB","").replace("$","").replace("USD",""))
#              left=data['Amount']
              depo=data.copy()
              spent=depo['Amount']
              if tran == "Spend in Spend" or tran == "Spend in Receive" : # Transaction is spend
                  out_spend.write (
                 """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s""" %data)
# if From followed by a To, don't write To here, wait next line
#                  if row<grid.grid_rows-1 and grid.grid_content(row+1,0).replace(' ','') != "": #if followed a new transaction then write out the current Credit transaction 
                  if row<grid.grid_rows-1 and grid.grid_contents[row+1][0].replace(' ','') != "": #if followed a new transaction then write out the current Credit transaction 
                     left=left-left
                     out_spend.write (
               """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s
               """ %depo)
                  elif row==grid.grid_rows-1:# write for last line
                     left=left-spent
                     out_spend.write (
               """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s
               """ %depo)
              elif tran == "Receive in Receive" or tran == "Receive in Spend" : # Transaction is Receive or Receive in Spend
                  out_receive.write (
                 """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s,%(PayMethod)s,%(CheckN)s,%(Notes)s """ %data)
# if From followed by a To, don't write To here, wait next line
#                  if row<grid.grid_rows-1 and mapping['FromAcc'](row+1,grid).replace(' ','') != "": #if followed a new transaction then write out the current Credit transaction 
                  if row<grid.grid_rows-1 and grid.grid_contents[row+1][0].replace(' ','') != "": #if followed a new transaction then write out the current Credit transaction 
                     left=left-left
                     out_receive.write (
               """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s,%(PayMethod)s,%(CheckN)s,%(Notes)s 
               """ %depo)
                  elif row==grid.grid_rows-1:# write for last line
                     left=left-spent
                     out_receive.write (
               """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s,%(PayMethod)s,%(CheckN)s,%(Notes)s 
               """ %depo)

           else: 

               from_or_to="to"
               depo=data.copy()    
               data['ToAcc']= "" 
               depo['Co./Last Name']= "" 
               depo['First Name']= "" 
               depo['FromAcc']= "" 
               spent=depo['Amount']
#               spent=float(depo['Amount'].replace("RMB","").replace("$","").replace("USD",""))
               left=left-spent

               if type_tran == "Spend" or tran == "Spend in Receive" : # Transaction is spend but in Receive file

                  out_spend.write (
                   """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s """ %depo)
                  if row<grid.grid_rows-1 and grid.grid_contents[row+1][0].replace(' ','') != "": #if followed a new transaction then write out the current Credit transaction 
#                  if row<grid.grid_rows-1 and mapping['FromAcc'](row+1,grid).replace(' ','') != "":
                     out_spend.write ("\n")

               else: # Transaction is Receive

                  out_receive.write (
                   """
%(FromAcc)s,%(Date)s,%(lname)s,%(fname)s,%(Memo)s,%(ToAcc)s, %(Amount)s,%(Currency)s, %(ExRate)s,%(PayMethod)s,%(CheckN)s,%(Notes)s  """ %depo)
                  if row<grid.grid_rows-1 and grid.grid_contents[row+1][0].replace(' ','') != "": #if followed a new transaction then write out the current Credit transaction 
#                  if row<grid.grid_rows-1 and mapping['FromAcc'](row+1,grid).replace(' ','') != "":
                     out_receive.write ("\n")

    out_receive.close()
    out_spend.close()
    return 0

