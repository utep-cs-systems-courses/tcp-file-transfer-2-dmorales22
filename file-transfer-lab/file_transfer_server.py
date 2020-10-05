#! /usr/bin/env python3

#Author: David Morales 
#Course: CS 4375 Theory of Operating Systems
#Instructor: Dr. Eric Freudenthal
#T.A: David Pruitt 
#Assignment: Project 2 
#Last Modification: 10/05/2020
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
        (('-d', '--debug'), "debug", False),
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

    while 1:
        conn, addr = s.accept()
        from framedSock import framedSend, framedReceive
        rc = os.fork()
        if rc == 0: 
            print('Connected by', addr)

            if os.path.exists("received_file") == True: #checks if filename is directory
                print("File exists. Overwriting original...")

            #filename_flag = bytes("FILE:", 'utf-8')

            with open("received_file", 'wb') as file: 
                while 1:
                    data = conn.recv(1024)
                    
                    if not data:
                        break
                    elif data == '':
                        print('Breaking from file write')
                        break
                    else: 
                        #data.replace(filename_flag, 'b''')
                        print(data)
                        file.write(data)

                file.close()

        if rc > 0:
            continue

    print("Got virus")
    conn.close()

def main():
    get_file()

main()