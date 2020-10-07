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

def get_file():
    switchesVarDefaults = (
        (('-l', '--listenPort') ,'listenPort', 50001),
        (('-d', '--debug'), "debug", False),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )

    progname = "file_transfer_server"
    paramMap = params.parseParams(switchesVarDefaults)
    listenPort = int(paramMap['listenPort'])
    listenAddr = ''  # Symbolic name meaning all available interfaces
    debug = paramMap['debug']

    if paramMap['usage']:
        params.usage()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Creates socket
    sock.bind((listenAddr, listenPort))                        # Binds socket
    sock.listen(1) # allow only one outstanding request
    print("Server is listening for clients...") # s is a factory for connected sockets

    while 1: #Runs infinite loop until user closes program
        conn, addr = sock.accept() #Accepts connection 
        from framedSock import framedSend, framedReceive
        rc = os.fork() #Forks to allow other clients

        if rc == 0: #Child process does all the file transfer 
            print('Connected by', addr)

            #msg = framedReceive(conn, debug)
            #filename = msg.split("!")

            if os.path.exists("received_file") == True: #Checks if filename is directory
                print("File exists. Overwriting original...")

            with open("received_file", 'wb') as file: #Creates file to write data to
                while 1:
                    data = framedReceive(conn, debug) #Receives data from client
                    if debug: #Debug info 
                        print("rec'd: ", data)
                    if not data: #Exits if data is null or non-existent 
                        if debug: 
                            print("child exiting")
                        sys.exit(0)
                    #data += b"!"                #Make emphatic!
                    framedSend(conn, data, debug) #Sends back to client if things are okay.
                    file.write(data) #Writes to file 

                file.close()

        if rc > 0: #Parent process continues loop to allow for more clients 
            continue

    conn.close()

def main():
    get_file()

main()