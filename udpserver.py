import socket
import threading
import hashlib 

def read_file(path,fileNo): # First we defined a function for reading files 
    packets = [] # create empty list for packets
    count = 0 # Create counter for packets
    with open(path, "rb") as file: # open file in binary mode for reading 
        data = file.read(8192) # Read 8192 bytes of file
        while data: # if data is not empty
            header = f"{fileNo}".encode() # create header for packet 
            if(fileNo < 10): # If file number is less than 10
                header = f"0{fileNo}".encode() # Create header with starting 0 to keep size of header consistent at 2 bytes
            packet = header + data # Create packet with header and data
            packets.append(packet) # Append packet to empty list we defined on line 6 
        
            data = file.read(8192) # Read 8192 bytes of file
            count += 1 # Increment counter after packet is read
    return packets # return file divided into packets

def interleavePacket(packets): # Function to mix file packets ensuring everyfile is transmitted almost at the same time
    interleavedPackets = [] # Create empty list for interleaved packets
    count = 0 # Created counter for packets
    maxLen = max([len(packet) for packet in packets]) # find maximum length of packets for
    for i in range(maxLen): 
        for packet in packets: # For each packet in packets
            if i < len(packet): # If packet is not empty
                interleavedPackets.append(packet[i]) # Append packet to interleaved packets
                count += 1 # Increment counter after packet is appended to interleaved packets 
    return interleavedPackets # return interleaved packets



def all_previous_acked(acknowledged, index): # Check if previous packets are acknowledged
    return all(acknowledged[:index]) # Return true if all packets before index are acknowledged

def send_func():
    global UDPServerSocket, send_base, next_seq_num, window_size, filePackets, address, lock, acknowledged # Initialize variables global 
    while send_base < len(filePackets): # While send base is less than length of packets
        with lock: # Lock the thread
            while next_seq_num < send_base + window_size and next_seq_num < len(filePackets): # While next sequence number is less than send base + window size and next sequence number is less than length of packets
                if next_seq_num >= len(acknowledged): # If next sequence number is greater than or equal to length of acknowledged
                    break
                if not acknowledged[next_seq_num]:
                    # Send packet without appending checksum multiple times
                    UDPServerSocket.sendto(filePackets[next_seq_num], address)
                  #  print("sending packet "+ str(next_seq_num))
                    start_timer(next_seq_num)  # Start timer for this packet
                next_seq_num += 1
    end_of_transmission = "EOT".encode()  # End Of Transmission message
    UDPServerSocket.sendto(end_of_transmission, address) # Send EOT message to client to indicate end of transmission



def recv_func(): # Function to receive packets from client
    global UDPServerSocket, address, send_base, filePackets, bufferSize, next_seq_num, lock, acknowledged
    while send_base < len(filePackets): ## while send base is less than length of packets
        message = UDPServerSocket.recvfrom(bufferSize)[0]  ## receive message from client
        if(message != b'000-1'):  # check if ack greater than -1 indicating ack received for valid packet
            ack = int(message)  ## convert ack to integer
        else:
            ack = -1
        with lock: ## lock the thread 
            if(ack!=-1):
                stop_timer(ack) # Stop timer for this packet
            if 0 <= ack < len(acknowledged): 
                acknowledged[ack] = True # Set packet as acknowledged
                if ack == send_base and all_previous_acked(acknowledged, ack): # If ack is equal to send base and all previous packets are acknowledged increase send base
                    send_base += 1 
                    while send_base < len(acknowledged) and acknowledged[send_base]: # Increments send base until it reaches a packet that is not acknowledged
                        send_base += 1 

def start_timer(packet_index): # Function to start timer for specific packet
    global timers 
    stop_timer(packet_index)  # Stop existing timer if any
    timer = threading.Timer(timeout, timeout_handler, [packet_index]) ## create timer for timeout
    timers[packet_index] = timer # Store timer in global list
    timer.start() # Start timer

def stop_timer(packet_index): # Function to stop timer for specific packet
    global timers
    if timers[packet_index] is not None: 
        timers[packet_index].cancel() ## cancel timer
        timers[packet_index] = None ## set timer to none

def timeout_handler(packet_index): # Function to handle timeout for specific packet
    global acknowledged, lock
    with lock: # Lock the thread
        if not acknowledged[packet_index]:  # If packet has not been acknowledged
            UDPServerSocket.sendto(filePackets[packet_index], address) # Resend packet
            start_timer(packet_index)  # Restart timer for this packet

def appendChecksums(packets):  # Function to append checksums to all packets
    index = 0
    for packet in packets:
        check = hashlib.md5(packet).digest() # Calculate checksum for packet
        packet = packet + check # Append checksum to end of packet
        packets[index] = packet 
        index+=1
        
        
#Main starts from here
#Initializing variables necessary for transmission
localIP     = "172.17.0.2"
localPort   = 20001
bufferSize  = 8192
send_base = 0
next_seq_num = 0
window_size = 4

# File preprocessing starts here
filePaths = ["/root/objects/small-0.obj", "/root/objects/large-0.obj","/root/objects/small-1.obj", "/root/objects/large-1.obj","/root/objects/small-2.obj", "/root/objects/large-2.obj","/root/objects/small-3.obj", "/root/objects/large-3.obj","/root/objects/small-4.obj", "/root/objects/large-4.obj","/root/objects/small-5.obj", "/root/objects/large-5.obj","/root/objects/small-6.obj", "/root/objects/large-6.obj","/root/objects/small-7.obj", "/root/objects/large-7.obj","/root/objects/small-8.obj", "/root/objects/large-8.obj","/root/objects/small-9.obj", "/root/objects/large-9.obj"]
filePackets = []

count = 0
for filePath in filePaths: # For each file path in file paths read file and append to file packets
    filePackets.append(read_file(filePath,count)) # append file to list
    count += 1

filePackets = interleavePacket(filePackets) # Interleave packets to ensure every file is transmitted almost at the same time


acknowledged = [False] * len(filePackets)  #  array to track acknowledgment for each packet
timers = [None] * len(filePackets)  # inşitialize timers for each packet

print("Number of packets prepared:", len(filePackets)) # Print number of packets prepared to terminal

lock = threading.Lock() ## create lock 

timer = None
timeout = 0.34 # Timeout duration in seconds calculated by RTT values 

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening") # Print message to terminal to show server is up and listening


index = 0
for packet in filePackets: # For each packet in file packets add header containing sequence number ensuring consistent size of header
    if index < 10:
        header = f"000{index}".encode()
    elif 10 <= index < 100:
        header = f"00{index}".encode()
    elif 100 <= index < 1000:
        header = f"0{index}".encode()
    else:
        header = f"{index}".encode()

    new_packet = header + packet
    filePackets[index] = new_packet
    index += 1

appendChecksums(filePackets) # Append checksums to all packets

bytesAddressPair = UDPServerSocket.recvfrom(bufferSize) # Receive initşal message from client
message = bytesAddressPair[0] 
address = bytesAddressPair[1] #extract client address
clientMsg = "Message from Client:{}".format(message)
clientIP  = "Client IP Address:{}".format(address)



print("Starting threads") # Print message to terminal to show threads are starting
# Start threads
sending_thread = threading.Thread(target=send_func)
recv_thread = threading.Thread(target=recv_func) 
sending_thread.start() 
recv_thread.start()  
sending_thread.join() # Wait for threads to finish  
recv_thread.join()  # Wait for threads to finish 
print("finished") # Print message to terminal to show transmission finished