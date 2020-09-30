#! /usr/bin/env python3

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

def get_file():
    switchesVarDefaults = (
        (('-l', '--listenPort') ,'listenPort', 50003),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )

    progname = "file_transfer_server"
    paramMap = params.parseParams(switchesVarDefaults)

    listenPort = int(paramMap['listenPort'])
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
    
    with open('file_from_client', 'wb') as file: 
        while 1:
            data = conn.recv(1024)
            if data == '':
                print('Breaking from file write')
                break
            else: 
                file.write(data)
            if not data:
                break

        file.close()

    print("Got virus")
    conn.close()
    
        
def main():
    get_file()

main()