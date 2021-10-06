ac2imp 

# From Bank output file to Accounting input file
This program generate two files for import to AccountEdge. The input file is a
modified from Bank output file or self manual entered transactions. The input
format is comma sperated csv file.

## Expens transactions
In detail, ac2imp will convert manual enter or manual changed of a transaction list
or bank export like Checking3.csv:
```
Checking Account,Date,Co./Last Name,First Name,Memo,Allocation Account #,Amount,Exchange Rate
11112, 03/06/2021,Carwell,Lydia,Lydia Salary in Feburary 2021, 61114  , RMB1200.00, 0.156006
# The following transaction is commented, and will not be loaded. 
#11104,7/13/21,Wells Fargo Bank,,ONLINE TRANSFER TO Jim,11105,-1000,,1
11104,6/8/21,,,ZELLE TO LAURA ON 06/08 REF #PP0BNM5326,61105,-500,1
11104,6/8/21,,,ZELLE TO LAURA ON 06/08 REF #PP0BNM5326,11105,-500,1
11104,9/17/21,,,ZELLE FROM LYNNE ON 09/17 REF # ST10GEKNSX2O,41090,500,1
```
into file format that importable to AccountEdge

it creats Spend list file Checking3_spend.txt:
```
Checking Account,Date,Co./Last Name,First Name, Memo,Allocation Account #,Amount,Currency Code, Exchange Rate
11112, 03/06/2021,Carwell,Lydia, Lydia Salary in Feburary 2021,, RMB1200.00,RMB, 0.156006
11112, 03/06/2021,,,Lydia Salary in Feburary 2021, 61114, RMB1200.00,RMB, 0.156006

11104,6/8/21,,,ZELLE TO LAURA ON 06/08 REF #PP0BNM5326,61105, -500.0,USD, 1
11104,6/8/21,,,ZELLE TO LAURA ON 06/08 REF #PP0BNM5326,61105, -500.0,USD, 1

11105,6/8/21,,,ZELLE TO LAURA ON 06/08 REF #PP0BNM5326,11104, 500.0,USD, 1
11105,6/8/21,,,ZELLE TO LAURA ON 06/08 REF #PP0BNM5326,11104, 500.0,USD, 1
```
Also generate Receiving file Checking3_receive.txt:
```
Deposit Account,Date,Co./Last Name,First Name,Memo,Allocation Account #,Amount,Currency Code,Exchange Rate,Payment Method,Check Number,Notes
11104,9/17/21,,,ZELLE FROM LYNNE ON 09/17 REF # ST10GEKNSX2O,41090, 500.0,USD, 1,Online Transfer,,
11104,9/17/21,,,ZELLE FROM LYNNE ON 09/17 REF # ST10GEKNSX2O,41090, 500.0,USD, 1,Online Transfer,,
```
1. by adding a Currency Code and generate a repeat line for deposit.

2. You can also have Receive Transactions in Spend Transactions as far as the
Allocation Account # start with '4' (Income accounts), like the 4th example above.

3. If the Amount is negative and Allocation Account # start with '6' (Expenses
accounts), this is the case of returned and refunded spend. The output will
keep the accounts sequence, but amount keeps negative.

4. However, if the amount is negative and Allocation Account # is NOT start with
'6', the Checking Account and Allocation Account will switch and the amount
becomes positive, as a normal spend transaction.

5. If the Exchange Rate is less than 1, the Currency Code is RMB, you can
change the code if your Currency is different from RMB.

6. Commented line start with '#' will not be converted.

## Bank export contains Debti and Credit columns
The export from bank usually have Debit and Credit columns, such as, Checking2.cvs
```
Checking Account,Date,Co./Last Name,First Name,Memo,Allocation Account #,Debit,Credit,Exchange Rate
11104,9/17/21,Wells Fargo Bank,,ZELLE FROM LYNNE ,41090,,500,1

11104,7/13/21,Wells Fargo Bank,,ONLINE TRANSFER TO LU Q,11105,-1000,,1

11112,6/9/2021,Liu,John,Bought 1 book Modern History,61190,70.24,, 0.152439

11113,6/9/2021,Liu,John,Returned Modern History book,61190,,70.24, 0.152439
```

It will turn into Checking2_spend.txt:
```
Checking Account,Date,Co./Last Name,First Name, Memo,Allocation Account #,Amount,Currency Code, Exchange Rate
11105,7/13/21,Wells Fargo Bank,,ONLINE TRANSFER TO LU Q,11104, 1000.0,USD, 1
11105,7/13/21,Wells Fargo Bank,,ONLINE TRANSFER TO LU Q,11104, 1000.0,USD, 1

61190,6/9/2021,Gavin,John,1 1 book return"Modern T History",11112, 70.24,RMB,  0.152439
61190,6/9/2021,Gavin,John,1 1 book return"Modern T History",11112, 70.24,RMB,  0.152439

11113,6/9/2021,Gavin,John,1 1 book return"Modern T History",61190, -70.24,RMB,  0.152439
11113,6/9/2021,Gavin,John,1 1 book return"Modern T History",61190, -70.24,RMB,  0.152439

61188,6/9/2021,,,1 book "T History",11115, 86.4,RMB, 0.152439
61188,6/9/2021,,,1 book "T History",11115, 86.4,RMB, 0.152439
```
and also generate Checking2_receive.txt:
```
Deposit Account,Date,Co./Last Name,First Name,Memo,Allocation Account #,Amount,Currency Code,Exchange Rate,Payment Method,Check Number,Notes
11104,9/17/21,Wells Fargo Bank,,ZELLE FROM LYNNE ,41090, 500.0,USD, 1,Online Transfer,,
11104,9/17/21,Wells Fargo Bank,,ZELLE FROM LYNNE ,41090, 500.0,USD, 1,Online Transfer,,
```

## Receive Money
Also for Received Donation, such as manual entered transactions list Receiving.csv:
```
Deposit Account,Date,Co./Last Name,First Name,Memo,Allocation Account #,Amount,Exchange Rate,Payment Method,Check Number
11109,1/4/21,Young,Y. Chris,Y. Chris Young,41090,$50.00,1.000000,10650924
11128,9/17/21,,,Pay William loan,11127,613.00,1.0,,
```
turns into Receiving_receive.txt:
```
Deposit Account,Date,Co./Last Name,First Name,Memo,Allocation Account #,Amount,Exchange Rate,Currency Code,Check Number,Notes
11109,1/4/21,Young,Y. Chris,Y. Chris Young,41090,$50.00,1.000000,USD,10650924,10650924
11109,1/4/21,Young,Y. Chris,Y. Chris Young,41090,$50.00,1.000000,USD,10650924,10650924
```
also Receiving_expense.txt:
```
Checking Account,Date,Co./Last Name,First Name, Memo,Allocation Account #,Amount,Currency Code, Exchange Rate
11128,9/17/21,,,Pay William loan,11127, 613.0,USD, 1.0
11128,9/17/21,,,Pay William loan,11127, 613.0,USD, 1.0
```

## Installation:

To install the program in your site packages, you can use
python to execute the install function:

> python3 setup.py install

This should work on both Windows, Mac and Linux.

## To run the program:

python3 /Library/Frameworks/Python.framework/Versions/3.6/bin/ac2imp

Or just run ac2imp

Runtime dependencies:

  wxPython.

Enjoy!

Contributors
Qiang Lu
