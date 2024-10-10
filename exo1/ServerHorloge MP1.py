import socket
import threading
import datetime

BUFFER_SIZE = 4096

def handle_client(client_socket):
    '''
    Handles client connections by receiving the number of requests, processing each one, and sending back the current time for valid requests.
    
    Parameters:
        client_socket: The socket object representing the client's connection.
    '''
    try:
        # Receive the request count from the client
        count_data = client_socket.recv(4)  # Expect 4 bytes (the integer)
        if not count_data:
            print("No data received, closing connection.")
            client_socket.close()
            return

        request_count = int.from_bytes(count_data, byteorder='big')
        print(f"Handling {request_count} requests from client")

        for i in range(request_count):
            # Receive request message from client
            client_message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            print(f"Received message: {client_message}")
            if client_message == "what time is it?":  # Check the exact question
                # Send the current time to the client in ISO format
                current_time = datetime.datetime.now().isoformat()
                client_socket.send(current_time.encode('utf-8'))
                print(f"Sent time to client: {current_time}")
            else:
                print(f"Unexpected message from client: {client_message}")

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()
        print("Closed connection to client")

def run_server(server_port=1236):
    '''
    Starts the server, listens for incoming client connections, and spawns a new thread for each client to handle concurrently.
    
    '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(5)
    print(f"Server ready for connection requests on port {server_port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection request from client {client_address}")

        # Handle each client in a separate thread
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    run_server()
