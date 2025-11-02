from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

tcpSerSock.bind(('', 8888))
tcpSerSock.listen(5)

while 1:
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    message = tcpCliSock.recv(1024)
    message = message.decode('utf-8')

    print(message)

    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)

    try:
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"

        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")
        tcpCliSock.send("\r\n")
        for line in outputdata:
            tcpCliSock.send(line)
        print('Read from cache')

    except IOError:
        if fileExist == "false":
            c = socket(AF_INET, SOCK_STREAM)
            
            hostn = filename.replace("www.","",1)
            print(hostn)

            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))

                # Create a temporary file on this socket and ask port 80
                # for the file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write("GET " + "http://" + filename + " HTTP/1.0\n\n")

                # Read the response into buffer
                buffer = fileobj.read()

                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket
                # and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                tcpCliSock.send(buffer)
                tmpFile.write(buffer)
                tmpFile.close()

            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            tcpCliSock.send("HTTP/1.0 404 Not Found\r\n")
            tcpCliSock.send("Content-Type:text/html\r\n")
            tcpCliSock.send("\r\n")
            tcpCliSock.send("<html><body><h1>404 Not Found</h1></body></html>")

    # Close the client and the server sockets
    tcpCliSock.close()
    # Fill in start.
    # (Keep the server socket open to accept more clients;
    #  do not close tcpSerSock inside the loop.)
    # Fill in end.
