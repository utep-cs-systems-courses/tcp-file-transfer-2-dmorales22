#! /usr/bin/env python3

#Author: David Morales 
#Course: CS 4375 Theory of Operating Systems
#Instructor: Dr. Eric Freudenthal
#T.A: David Pruitt 
#Assignment: Project 2 
#Last Modification: 10/18/2020
#Purpose: File transfer program (server w/ threading)

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from threading import Thread, Lock
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
sock.listen(5)
print("Server is listening for clients...") # s is a factory for connected sockets

if os.path.isdir("received_files") == False: #Checks if directory where received files are stored exists.
    os.mkdir("received_files") #Creates directory if it doesn't exist

lock = Lock() #Creates the lock
active_files = [] #Creating list to keep track of active files within the lock

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print('Connected by', self.addr)
        file_info = self.fsock.receive(debug).decode("utf-8").split(":") #First receives filename and file size from client. 
        filename, file_size_str = file_info[0], file_info[1]
        print("File receiving: '" + filename + "' Size: " + file_size_str)
        file_size = int(file_size_str)

        if os.path.exists("received_files/" + filename) == True: #Checks if filename is in the directory
            self.fsock.send(b'1', debug) #Sends back to client that file exists on server directory
            print("File exists. Overwriting original...")

        else:
            self.fsock.send(b'0', debug) #Sends back to client that file does not exist on server directory

        lock.acquire() #Gets lock to check active files 

        if filename in active_files: #If filename is in the list, then it will exit out. 
            print("Cannot complete transfer. File is active.")
            self.fsock.close()
            lock.release()
            return

        else: #Adds file name to active list 
            active_files.append(filename)

        lock.release() #Releases lock to resume normal function

        with open("received_files/" + filename, 'wb') as file: #Creates file to write data to
            while 1:
                data = self.fsock.receive(debug) #Receives data from client

                if debug: #Debug info 
                    print("Data received: ", data)

                if not data: #Exits if data is None type, non-existent, or end of file
                    if file_size == os.path.getsize("received_files/" + filename):
                        print("File: '" + filename + "' received!")

                    else: 
                        print("File is incomplete due to a dropped connection. Transfer incomplete!")

                    lock.acquire() 
                    active_files.remove(filename) #Removes active file(name) from list within lock
                    lock.release()

                    if debug: 
                        print(f"thread connected to {addr} done")

                    self.fsock.close() #Close connection
                    file.close()
                    return

                file.write(data) #Writes to file 
                self.fsock.send(data, debug) #Sends response back to client

while 1: #Runs infinite loop until server is closed. 
    sockAddr = sock.accept()
    server = Server(sockAddr)
    server.start()