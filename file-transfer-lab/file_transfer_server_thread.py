#! /usr/bin/env python3

#Author: David Morales 
#Course: CS 4375 Theory of Operating Systems
#Instructor: Dr. Eric Freudenthal
#T.A: David Pruitt 
#Assignment: Project 2 
#Last Modification: 10/14/2020
#Purpose: File transfer program (server)

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from threading import Thread
from encapFramedSock import EncapFramedSock

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "file_transfer_server_thread"
paramMap = params.parseParams(switchesVarDefaults)
listenPort = int(paramMap['listenPort'])
listenAddr = ''  # Symbolic name meaning all available interfaces
debug = paramMap['debug']

if paramMap['usage']:
    params.usage()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Creates socket
sock.bind((listenAddr, listenPort))                        # Binds socket
sock.listen(5) # allow only one outstanding request
print("Server is listening for clients...") # s is a factory for connected sockets

if os.path.isdir("received_files") == False: #Checks if directory where recieved files are stored exists.
    os.mkdir("received_files") #Creates directory if it doesn't exist

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print('Connected by', self.addr)
 
        filename_byte = self.fsock.receive(debug) #First recieves filename from client
        filename = filename_byte.decode("utf-8")
        print("File receiving: " + filename)

        if os.path.exists("received_files/" + filename) == True: #Checks if filename is directory
            self.fsock.send(b'1', debug) #Sends back to client that file exists on server directory
            print("File exists. Overwriting original...")

        else:
            self.fsock.send(b'0', debug) #Sends back to client that file does not exist on server directory

        with open("received_files/" + filename, 'wb') as file: #Creates file to write data to
            while 1:
                data = self.fsock.receive(debug) #Receives data from client

                if debug: #Debug info 
                    print("rec'd: ", data)
                if not data: #Exits if data is null or non-existent 
                    if debug: 
                        print(f"thread connected to {addr} done")
                    self.fsock.close() #Close connection
                    return

                self.fsock.send(data, debug)
                file.write(data) #Writes to file 

            file.close()
        self.fsock.close()

while 1:
    sockAddr = sock.accept()
    server = Server(sockAddr)
    server.start()