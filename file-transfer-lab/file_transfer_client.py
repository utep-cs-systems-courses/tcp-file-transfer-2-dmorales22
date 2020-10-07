#! /usr/bin/env python3

#Author: David Morales 
#Course: CS 4375 Theory of Operating Systems
#Instructor: Dr. Eric Freudenthal
#T.A: David Pruitt 
#Assignment: Project 2 
#Last Modification: 10/05/2020
#Purpose: File transfer program (client)

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from framedSock import framedSend, framedReceive

def send_file():
    switchesVarDefaults = (
        (('-s', '--server'), 'server', "127.0.0.1:50000"),
        (('-f', '--file'), 'filename', 'testfile'),
        (('-d', '--debug'), "debug", False),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )


    progname = "file_transfer_client"
    paramMap = params.parseParams(switchesVarDefaults)

    server, usage, filename, debug = paramMap["server"], paramMap["usage"], paramMap["filename"], paramMap["debug"]

    if usage:
        params.usage()

    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    addrFamily = socket.AF_INET
    socktype = socket.SOCK_STREAM
    addrPort = (serverHost, serverPort)
    sock = socket.socket(addrFamily, socktype)

    if sock is None: #If cannot open socket
        print('could not open socket')
        sys.exit(1)

    sock.connect(addrPort)

    if os.stat(filename).st_size == 0: #Checks if file is empty and rejects it
        print("No zero length files allowed. Try again.")
        sock.close()
        sys.exit(1)

    try: 
        with open(filename, 'rb') as file: #Opens file to read
            while True:
                data = file.read(1024) #Reads file by 1024 bytes
                framedSend(sock, data, debug) #Sends data 
                if not data:
                    break 
                print("received:", framedReceive(sock, debug)) #Checks if server is okay
            file.close()
            print("Sent file!")

    except FileNotFoundError: #If file is not found
        print("File not found. Try again.")

    sock.close()

def main():
    send_file()

main()