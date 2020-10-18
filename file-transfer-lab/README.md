# File Transfer Program (Forked & Threaded) 
Note: This program designed and written for Unix-based systems and will not work correctly in Windows. This is a Python 3 program.

This is a simple TCP file transfer program that uses forking and threading (separate programs). The client provided here should work with both versions of the server with effective error handling on both ends. These Python programs are based off the demo code provided by Dr. Eric Freudenthal. The demo code can be found in this repository. 

## Usage
This can work with the proxy provided (stammerProxy.py) in this repository, you just have to connect to the proxy server's IP address and port. 

### Client Usage: 
The client by default will try to connect to the proxy (so run stammerProxy.py first). Or specify the server's IP address and port if you want to connect directly to the server, or connect to the proxy at a different location. 

`-s` or `--server`: Connects to the specified server's IP address and port in the command line arguments. Example `-s 127.0.0.1:50000` in this format.

`-f` or `--file`: Specifies the name of the file you want to send. Example `-f testfile.txt` in this format. 

`-r` or `--remote`: Specifies filename you want on the server received files directory (renames the sent file). Example `-r renamed_testfile.txt` in this format.

`-d` or `--debug`: If you want to use debug mode.

`-?` or `--usage` or `-h`: To see the usage parameters.

### Server Usage: 
The server (both versions) by default will run on `127.0.0.1:50001`. Another thing to note is that the server stores files in an automatically created directory called `received_files/` within the same directory the server script is in. Incomplete files (due to lost connection) are not deleted, but are warned of in the server console.  

`-l` or `--listenPort`: To specify a port you want to use. Example `-l 50002` in this format. 

`-d` or `--debug`: If you want to use debug mode. 

`-?` or `--usage` or `-h`: To see the usage parameters.