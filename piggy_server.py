import socket
import sqlite3
import json

conn = sqlite3.connect("piggybank.db")
cursor = conn.cursor()

pins = {}
account_balance = {}
names = {}
account_no = {}
trxn_id = []

for t in cursor.execute('select * from Trxn'):
    trxn_id.append(t[0])

for x in cursor.execute('select * from Customers'):
    pins[x[0]] = x[9]

for i in cursor.execute('select * from customers_account'):
    account_balance[i[0]] = i[3]

for i in cursor.execute('select * from customers_account'):
    names[i[0]] = i[1]

for y in cursor.execute('select * from customers_account'):
    account_no[y[0]] = y[4]

cursor.close()
conn.close()

# print(trxn_id)
# print(pins)
# print(account_balance)
# print(names)
# print(account_no)

packaged_pins = str.encode(json.dumps(pins))
packaged_balance = str.encode(json.dumps(account_balance))
packaged_names = str.encode(json.dumps(names))
packaged_accountNo = str.encode(json.dumps(account_no))
packaged_trxn = str.encode(json.dumps(trxn_id))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 5424
server.bind((host, port))
server.listen()


while True:

    print(f'server started, running on port{port}')
    client, addr = server.accept()
    client.send(str.encode(f'Accepted connection from {addr}'))

    while True:
        request = bytes.decode(client.recv(1024)).lower()
        if request == 'pin':
            client.send(packaged_pins)
        elif request == 'balance':
            client.send(packaged_balance)
        elif request == 'names':
            client.send(packaged_names)
        elif request == 'acct':
            client.send(packaged_accountNo)
        elif request == 'trxn':
            client.send(packaged_trxn)
        elif request == 'q':
            print(f'disconnecting from {addr}')
            break
        else:
            print('invalid request')
            print(f'disconnecting from {addr}')
            break

    if input('enter q to stop').upper() == 'Q':
        break
