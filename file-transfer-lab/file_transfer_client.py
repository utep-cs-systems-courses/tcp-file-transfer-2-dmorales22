#! /usr/bin/env python3


import socket, sys, re
sys.path.append("../lib")       # for params
import params

def send_file():
    switchesVarDefaults = (
        (('-s', '--server'), 'server', "127.0.0.1:50001"),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )


    progname = "file_transfer_client"
    paramMap = params.parseParams(switchesVarDefaults)

    server, usage  = paramMap["server"], paramMap["usage"]

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

    outMessage = b"Hello world!"

    print("sending '%s'" % outMessage)
    sendAll(s, outMessage)

    data = s.recv(1024).decode()
    print("Received '%s'" % data)

    print("sending '%s'" % outMessage)
    sendAll(s, outMessage)

    s.shutdown(socket.SHUT_WR)      # no more output

    while 1:
        data = s.recv(1024).decode()
        print("Received '%s'" % data)
        if len(data) == 0:
            break
    print("Zero length read.  Closing")
    s.close()

def main()
    send_file()

main()
