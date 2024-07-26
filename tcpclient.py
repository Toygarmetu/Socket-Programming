import socket
import time

HOST = "172.17.0.2"  # The server's IP address
PORT = 65422 # The port used by the server 

## first we defined a function for receiving file from server

def receive_file(socket): ## receive file from server
    data = socket.recv(1024) ## receive 1024 bytes
    while data: ## if data is not empty
        data = socket.recv(1024) ## receive 1024 bytes
        if data == b"EOF": ## if data is EOF
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: ## create socket
    s.connect((HOST, PORT)) ## connect to server
    start_time = time.time()  # Start timing
    receive_file(s)  # Receive and save small file
    receive_file(s)  # Receive and save large file
    receive_file(s)  # Receive and save small file
    receive_file(s)  # Receive and save large file
    receive_file(s)  # Receive and save small file
    receive_file(s)  # Receive and save large file
    receive_file(s)  # Receive and save small file
    receive_file(s)  # Receive and save large file
    receive_file(s)  # Receive and save small file
    receive_file(s)  # Receive and save large file
    receive_file(s)  # Receive and save small file
    receive_file(s)  # Receive and save large file
    receive_file(s)  # Receive and save small file
    receive_file(s)  # Receive and save large file
    receive_file(s)  # Receive and save small file
    receive_file(s)  # Receive and save large file
    receive_file(s)  # Receive and save small file
    receive_file(s)  # Receive and save large file
    receive_file(s)  # Receive and save small file
    receive_file(s)  # Receive and save large file
    
    end_time = time.time()  # End timing
    print(f"Transmission ended. Duration: {end_time - start_time} seconds")  # Printed duration for report



