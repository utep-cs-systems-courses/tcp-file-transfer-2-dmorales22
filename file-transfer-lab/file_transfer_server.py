#! /usr/bin/env python3

#Author: David Morales 
#Course: CS 4375 Theory of Operating Systems
#Instructor: Dr. Eric Freudenthal
#T.A: David Pruitt 
#Assignment: Project 2 
#Last Modification: 09/30/2020
#Purpose: File transfer program (server)

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

def sendAll(sock, buf):
    while len(buf):
        print(f"trying to send <{buf}>...")
        nbytes = sock.send(buf)
        print(f" {nbytes} bytes sent, {len(buf) - nbytes} bytes remain")
        buf = buf[nbytes:]

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


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Creates socket
    s.bind((listenAddr, listenPort))                        # Binds socket
    s.listen(1)                                             # allow only one outstanding request
    print("Server is listening for clients...")
    # s is a factory for connected sockets

    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    print('Connected by', addr)

    if os.path.exists("received_file") == True: #checks if filename is directory
        print("File exists. Overwriting original...")


    with open("received_file", 'wb') as file: 
        while 1:
            data = conn.recv(1024)
            if not data:
                break
            if data == '':
                print('Breaking from file write')
                break
            else: 
                file.write(data)

        file.close()

    print("Got virus")
    conn.close()

def main():
    get_file()

main()