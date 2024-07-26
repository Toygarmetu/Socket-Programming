import socket

HOST = "172.17.0.2"   # The server's IP address
PORT = 65422  # The port used by the server 

# first we defined a function for sending file to client

def send_file(path, socket): # send file to client
    with open(path, "rb") as file: # open file in binary mode
        data = file.read(1024) # read 1024 bytes 
        while data: # if data is not empty
            socket.sendall(data) # send data to client
            data = file.read(1024) # read 1024 bytes of file
    socket.sendall(b"EOF") # send EOF to indicate end of file
        
    
## then we defined a function for receiving file from client

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # create socket 
    s.bind((HOST, PORT)) # bind socket to address
    s.listen() # listen for connections
    conn, addr = s.accept() # accept connection
    with conn: # when connection is accepted
        send_file("/root/objects/small-0.obj", conn) ## send small file
        send_file("/root/objects/large-0.obj", conn) ## send large file
        send_file("/root/objects/small-1.obj", conn) ## send small file
        send_file("/root/objects/large-1.obj", conn) ## send large file
        send_file("/root/objects/small-2.obj", conn) ## send small file
        send_file("/root/objects/large-2.obj", conn) ## send large file
        send_file("/root/objects/small-3.obj", conn) ## send small file
        send_file("/root/objects/large-3.obj", conn) ## send large file
        send_file("/root/objects/small-4.obj", conn) ## send small file
        send_file("/root/objects/large-4.obj", conn) ## send large file
        send_file("/root/objects/small-5.obj", conn) ## send small file
        send_file("/root/objects/large-5.obj", conn) ## send large file
        send_file("/root/objects/small-6.obj", conn) ## send small file
        send_file("/root/objects/large-6.obj", conn) ## send large file
        send_file("/root/objects/small-7.obj", conn) ## send small file
        send_file("/root/objects/large-7.obj", conn) ## send large file
        send_file("/root/objects/small-8.obj", conn) ## send small file
        send_file("/root/objects/large-8.obj", conn) ## send large file
        send_file("/root/objects/small-9.obj", conn) ## send small file
        send_file("/root/objects/large-9.obj", conn) ## send large file

