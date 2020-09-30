#! /usr/bin/env python3

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

def get_file():
    switchesVarDefaults = (
        (('-l', '--listenPort') ,'listenPort', 50001),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )

    progname = "file_transfer_server"
    paramMap = params.parseParams(switchesVarDefaults)

    listenPort = paramMap['listenPort']
    listenAddr = ''       # Symbolic name meaning all available interfaces

    if paramMap['usage']:
        params.usage()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((listenAddr, listenPort))
    s.listen(1)              # allow only one outstanding request
    print("Server is listening for clients...")
    # s is a factory for connected sockets

    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    print('Connected by', addr)
    while 1:
        data = conn.recv(1024).decode()
        if not data: 
            break

        filename = "testfile"
        file = open(filename,'rb')
        stream = file.read(1024)
        while stream:
            conn.send(stream)
            stream  = f.read(1024)
        file.close()

    print("Got file!")
    conn.send("Got free virus. Thank you.")
    conn.close()

def main():
    get_file()

main()