#!/usr/bin/python3

import returnify,sys
from bitcoinrpc.authproxy import *
from bitcoin import *

def toBinary(string):
    return "".join([format(ord(char),'#010b')[2:] for char in string])

rpc_user = 'username'
rpc_password = 'password'
port=43123
#print(sys.argv[1])
amount = decimal.Decimal(sys.argv[1])#(input("Enter amount of coins to lose: "))
txfee = decimal.Decimal(0.01)#(input("Enter txfee: "))

con = AuthServiceProxy("http://%s:%s@127.0.0.1:%i"%(rpc_user, rpc_password,port))

#listunspent
listun = con.listunspent(0)

for i in range(len(listun)):
    #print (listun[i]['amount'])
    if not listun[i]['amount'] < amount+txfee:
            #print("Found a good one: %s with amount %i"%(listun[i]['txid'],listun[i]['amount']))
                change = listun[i]['address']
                listun = listun[i]
                vout = listun['vout']
                txid = listun['txid']
                break
        

#lost = str(input("Please enter the bitcoin address to send coins (will be lost!): "))
lost=str(sys.argv[2])#(input("Enter address to send lost coins (must be different from return address): "))
changeamount = listun['amount']-(amount+txfee)
#print(changeamount)
#print(txfee)
#print(txid)
#print(vout)
#print([{"txid":txid,"vout":vout}], {lost:amount,change:changeamount})
#print(lost,amount)

raw = con.createrawtransaction([{"txid":txid,"vout":vout}], {lost:amount,change:changeamount})
deser = deserialize(raw)
#print(deser)

#creating the script
#to be created!
hexscript=returnify.returnify(str(sys.argv[3]))#(input("String to be encoded: ")))

#finding n replacing script
for i in range(len(deser['outs'])):
    if int(deser['outs'][i]['value']) == amount*100000000:
        goodout = i
        deser['outs'][i]['script'] = hexscript

#serializing n signing
ser = serialize(deser)
signed = con.signrawtransaction(ser)
signed = signed['hex']
#print(signed)
print(deserialize(signed))

#sending transaction
sure = str(input("Are you sure you want to send the transaction? (y/n): "))

if(sure=="y"):
    con.sendrawtransaction(signed)
else:
    print("Exiting..")
