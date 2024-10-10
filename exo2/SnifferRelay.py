import socket
import threading

BUFFER_SIZE = 4096
log_file = "http_sniffer_log.txt"

def log_request(client_ip, uri, server_response):
    '''
    Logs each client request and the server's response to a file.
    
    Parameters:
        client_ip: The IP address of the client making the request.
        uri: The requested URI.
        server_response: The HTTP response received from the server.
'''
    with open(log_file, "a") as log:
        log.write(f"Client IP: {client_ip}, URI: {uri}\nResponse: {server_response}\n\n")

def handle_client(client_socket, client_address, server_ip, server_port):
    '''
    Handles client requests, relays them to the server, logs the request and response, and sends the server’s response back to the client.

    Parameters:
        client_socket: The socket object for the client connection.
        client_address: The client's IP address.
        server_ip: IP address of the server.
        server_port: Port number of the server.
        
    '''
    request = client_socket.recv(BUFFER_SIZE).decode("utf-8")
    print(f"Received request:\n{request}")

    if request.startswith("GET"):
        uri = request.split(" ")[1]

        # Relay the request to the actual server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((server_ip, server_port))
        server_socket.send(request.encode("utf-8"))

        # Get server response
        response = server_socket.recv(BUFFER_SIZE)
        server_socket.close()

        # Log the request and response
        log_request(client_address[0], uri, response.decode("utf-8"))

        # Send the response back to the client
        client_socket.sendall(response)

    client_socket.close()

def run_sniffer_relay(relay_port=5556, server_ip='localhost', server_port=5557):
    '''
    Starts the sniffer relay server, listens on a port for incoming connections, and creates threads to handle each connection.

    Parameters:
        relay_port: Port on which the sniffer relay listens.
        server_ip: IP address of the upstream server.
        server_port: Port number of the upstream server.
        
    '''
    relay_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relay_socket.bind(('', relay_port))
    relay_socket.listen(5)
    print(f"Sniffer Relay listening on port {relay_port}...")

    while True:
        client_socket, client_address = relay_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address, server_ip, server_port)).start()

if __name__ == "__main__":
    run_sniffer_relay()
