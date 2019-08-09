#!/usr/bin/python3

import returnify,sys
from bitcoinrpc.authproxy import *
from bitcoin import *
from binascii import unhexlify

def toBinary(string):
    return ''.join([format(ord(char),'#010b')[2:] for char in string])

rpc_user = 'rpcuser'
rpc_password = 'rpcpass'
port=62541

transaction = sys.argv[1]

con = AuthServiceProxy('http://%s:%s@127.0.0.1:%i'%(rpc_user, rpc_password,port))

tx = con.getrawtransaction(transaction, 1)

outputs = tx['vout']

encoded = [unhexlify(output['scriptPubKey']['asm'][10:]).decode('ascii') for output in outputs if output['scriptPubKey']['asm'].startswith('OP_RETURN ')]

print('Data encoded in this transaction:\n')
print('\n'.join(encoded))