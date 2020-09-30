#! /usr/bin/env python3


import socket, sys, re
sys.path.append("../lib")       # for params
import params

def send_file():
    switchesVarDefaults = (
        (('-s', '--server'), 'server', "127.0.0.1:50003"),
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

    with open("testfile", 'rb') as file:
        s.send(b'BEGIN')
        while True:
            data = file.read(1024)
            s.send(data)
            if not data:
                break 
        s.send(b'ENDED')
        file.close()

    print("Sent file!")
    s.close()

def main():
    send_file()

main()
