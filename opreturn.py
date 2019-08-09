#!/usr/bin/python3

import returnify,sys
from bitcoinrpc.authproxy import *
from bitcoin import *

def toBinary(string):
    return "".join([format(ord(char),'#010b')[2:] for char in string])

rpc_user = 'rpcuser'
rpc_password = 'rpcpass'
port=62541

txfee = decimal.Decimal(0.01)

con = AuthServiceProxy("http://%s:%s@127.0.0.1:%i"%(rpc_user, rpc_password,port))

listun = con.listunspent(0)

for i in range(len(listun)):
    if not listun[i]['amount'] < txfee:
        change = listun[i]['address']
        listun = listun[i]
        vout = listun['vout']
        txid = listun['txid']
        break
        

lost=str(sys.argv[1])
changeamount = listun['amount']-txfee

raw = con.createrawtransaction([{"txid":txid,"vout":vout}], {lost:0.00000001,change:changeamount})
deser = deserialize(raw)

hexscript=returnify.returnify(str(sys.argv[2]))#(input("String to be encoded: ")))

for i in range(len(deser['outs'])):
    if int(deser['outs'][i]['value']) == 1:
        goodout = i
        deser['outs'][i]['value'] = 0
        deser['outs'][i]['script'] = hexscript

ser = serialize(deser)
signed = con.signrawtransaction(ser)
signed = signed['hex']

print(deserialize(signed))

sure = str(input("Are you sure you want to send the transaction? (y/n): "))

if(sure=="y"):
    print("Sending transaction...")
    txid = con.sendrawtransaction(signed)
    print("Transaction sent. ID: " + txid)
else:
    print("Exiting..")
