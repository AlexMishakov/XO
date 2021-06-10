#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen()
conn, addr = sock.accept()

print('connected:', addr)

while True:
    data = conn.recv(1024)
    if data:
        print(data.decode())
    #conn.send(data.upper())

conn.close()