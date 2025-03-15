import socket
import threading

receivedDataStringFromPYNQ = ""
receivedDataStringFromDestinationHost = ""
isConnected = False

# Server configuration which pynq board will use
server_host = '192.168.0.4'
server_port = 8080
    
# Client configuration
client_host = '137.110.39.253' #Ip of Destination host
client_port = 8080  # port for client to connect to the destination host

# Server Function for PYNQ side handling
def start_server_4pynq_side(server_socket,client_socket_4host_side,fork):

    # Bind and listen
    server_socket.bind((server_host, server_port))
    server_socket.listen(1)
    print(f"Server listening on {server_host}:{server_port}...")

    # Accept incoming connection
    pynq_side_conn_handle, pynq_client_address = server_socket.accept()
    print(f"Server connected to {pynq_client_address}")

    global receivedDataStringFromPYNQ
    global receivedDataStringFromDestinationHost
    #global as_client_socket
    
    # Communicate with the client
    while True:
        try:
            data = pynq_side_conn_handle.recv(1024)
            if not data:
                break
            receivedDataStringFromPYNQ = data.decode()
            print(f"Server received from PYNQ: {receivedDataStringFromPYNQ}")
            
            #now need to pass this to other PC, but only if it has got connection
            if fork.acquire():
                #this means connection is available
                print("client side has connection")
                client_socket_4host_side.sendall(receivedDataStringFromPYNQ.encode())
                print(f"Message sent to Destination PC: {receivedDataStringFromPYNQ}")
                fork.release()
                data = client_socket_4host_side.recv(1024)
                if not data:
                    break
                receivedDataStringFromDestinationHost = data.decode()
                
                #now forward it to PYNQ
                pynq_side_conn_handle.sendall(receivedDataStringFromDestinationHost.encode())
                print("Resending Data from PYNQ")
        except Exception as e:
            print(f"Server error: {e}")
            break
    
    # Close the server connection
    pynq_side_conn_handle.close()
    server_socket.close()
    client_socket_4host_side.close()

# Client Function
def start_client_4_Dest_PC(client_socket_4host_side,fork):

    global receivedDataStringFromDestinationHost
    #global isConnected
    
    #while True: #can create an exit
    try:
        # Connect to the server
        client_socket_4host_side.connect((client_host, client_port))
        print(f"Client connected to {client_host}:{client_port}")
        fork.release() # release the lock to inform server side now communication can happen

    except Exception as e:
        print(f"Client error: {e}")
    #nothing to be done at client once connection opens

# Main function to start both server and client
if __name__ == '__main__':
    # Create client socket
    client_socket_4host_side = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    fork = threading.Lock()
    fork.acquire() #taking the lock even before server has started
    
    # Create server socket
    server_socket_4pynq_side = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server_4pynq_side,args=(server_socket_4pynq_side,client_socket_4host_side,fork))
    server_thread.start()

    # Start client after a short delay to give server time to start
    import time
    time.sleep(1)

    start_client_4_Dest_PC(client_socket_4host_side,fork)

