#! /usr/bin/env python3

#Author: David Morales 
#Course: CS 4375 Theory of Operating Systems
#Instructor: Dr. Eric Freudenthal
#T.A: David Pruitt 
#Assignment: Project 2 
#Last Modification: 09/30/2020
#Purpose: File transfer program (client)

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params

def sendAll(sock, buf):
    while len(buf):
        print(f"trying to send <{buf}>...")
        nbytes = sock.send(buf)
        print(f" {nbytes} bytes sent, {len(buf) - nbytes} bytes remain")
        buf = buf[nbytes:]

def send_file():
    switchesVarDefaults = (
        (('-s', '--server'), 'server', "127.0.0.1:50003"),
        (('-f', '--file'), 'filename', 'testfile'),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )


    progname = "file_transfer_client"
    paramMap = params.parseParams(switchesVarDefaults)

    server, usage, filename = paramMap["server"], paramMap["usage"], paramMap["filename"]

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

    s = socket.socket(addrFamily, socktype)
    if s is None:
        print('could not open socket')
        sys.exit(1)

    s.connect(addrPort)

    if s is None:
        print('could not open socket')
        sys.exit(1)


    if os.stat(filename).st_size == 0:
        print("No zero length files allowed. Try again.")
        s.close()
        sys.exit(1)

    try:
        with open(filename, 'rb') as file:
            while True:
                data = file.read(1024)
                s.send(data)
                if not data:
                    break 
            file.close()
            print("Sent file!")

    except FileNotFoundError:
        print("File not found. Try again.")
    s.close()


def main():
    send_file()

main()
