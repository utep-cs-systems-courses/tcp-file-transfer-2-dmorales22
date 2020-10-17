#! /usr/bin/env python3

#Author: David Morales 
#Course: CS 4375 Theory of Operating Systems
#Instructor: Dr. Eric Freudenthal
#T.A: David Pruitt 
#Assignment: Project 2 
#Last Modification: 10/16/2020
#Purpose: File transfer program (server w/ forks)

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

def get_file():
    switchesVarDefaults = (
        (('-l', '--listenPort') ,'listenPort', 50001),
        (('-d', '--debug'), "debug", False),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )

    progname = "file_transfer_server_forked"
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

    if os.path.isdir("received_files") == False: 
        os.mkdir("received_files")

    while 1: #Runs infinite loop until user closes program
        conn, addr = sock.accept() #Accepts connection 
        from framedSock import framedSend, framedReceive
        rc = os.fork() #Forks to allow other clients

        if rc == 0: #Child process does all the file transfer 
            print('Connected by', addr)
            file_info = framedReceive(conn, debug).decode("utf-8").split(":") #First receives filename from client
            filename, file_size_str = file_info[0], file_info[1]
            print("File receiving: '" + filename + "' Size: " + file_size_str)

            file_size = int(file_size_str)

            if os.path.exists("received_files/" + filename) == True: #Checks if filename is directory
                framedSend(conn, b'1', debug)
                print("File exists. Overwriting original...")

            else:
                framedSend(conn, b'0', debug) #Sends back to client that file does not exist on server directory

            with open("received_files/" + filename, 'wb') as file: #Creates file to write data to
                while 1:
                    data = framedReceive(conn, debug) #Receives data from client

                    if debug: #Debug info 
                        print("Data received: ", data)

                    if not data: #Exits if data is None type or non-existent 
                        if file_size == os.path.getsize("received_files/" + filename): #Checks if file is complete by comparing sizes 
                            print("File: '" + filename + "' received!")

                        else: 
                            print("File is incomplete due to a dropped connection. Transfer incomplete!")

                        if debug: 
                            print("Child exiting!")

                        sys.exit(0)

                    file.write(data) #Writes to file 
                    framedSend(conn, data, debug) #Sends response back to client
                file.close() #Closes file writer
            conn.close()

        if rc > 0: #Parent process continues loop to allow for more clients 
            continue

    conn.close()

get_file()