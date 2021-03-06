#! /usr/bin/env python3

#Author: David Morales 
#Course: CS 4375 Theory of Operating Systems
#Instructor: Dr. Eric Freudenthal
#T.A: David Pruitt 
#Assignment: Project 2 
#Last Modification: 10/18/2020
#Purpose: File transfer program (client)

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from framedSock import framedSend, framedReceive

def send_file():
    switchesVarDefaults = ( 
        (('-s', '--server'), 'server', "127.0.0.1:50000"),
        (('-f', '--file'), 'filename', 'testfile'),
        (('-r', '--remote'), 'filename_r','testfile'), 
        (('-d', '--debug'), "debug", False),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )

    progname = "file_transfer_client"
    paramMap = params.parseParams(switchesVarDefaults)

    server, usage, filename, debug, filename_r = paramMap["server"], paramMap["usage"], paramMap["filename"], paramMap["debug"], paramMap["filename_r"] #Getting parameters usage from args

    if usage:
        params.usage()

    try: #Tries to parse server name 
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    addrFamily = socket.AF_INET #Creates socket 
    socktype = socket.SOCK_STREAM
    addrPort = (serverHost, serverPort)
    sock = socket.socket(addrFamily, socktype)

    if sock is None: #If cannot open socket
        print("Could not open socket!")
        sys.exit(1)

    sock.connect(addrPort)

    if os.stat(filename).st_size == 0: #Checks if file is empty and rejects it
        print("No zero length files allowed. Try again.")
        sock.close()
        sys.exit(1)

    file_size = os.path.getsize(filename) #Gets file size 

    if filename_r == "testfile": #If remote usage is default 
        filename_r = filename

    framedSend(sock, bytes(filename_r + ":" + str(file_size), 'utf-8'), debug) #Sends filename to server
    file_exists = framedReceive(sock, debug) #Gets response from server if file exists
    print("Sending file: '" + filename + "', Remote name: '" + filename_r + "'")

    if file_exists == b'1': #If file exists on server
        print("File exists. Will override...")

    try: 
        with open(filename, 'rb') as file: #Opens file to read
            while True:
                data = file.read(16384) #Reads file by 16384 bytes (16kB)
                framedSend(sock, data, debug) #Sends data

                if not data: #Breaks if data is None type
                    break

                data_sent = framedReceive(sock, debug) #Saves server response

                if data != data_sent: #Checks if response from the server is a complete message
                    print("Transfer failed! Connection was dropped or file active.")
                    file.close()
                    sock.close()
                    sys.exit(0)

                if debug:
                    print("Data sent: ", data_sent)

            print("File: '" + filename + "' sent!")
            file.close() #Closes file reader

    except FileNotFoundError: #If file is not found
        print("File not found. Try again.")

    sock.close()

send_file()