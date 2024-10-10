import socket
import threading

BUFFER_SIZE = 4096
forbidden_sites = ["bannedforloubar.com", "bannedforkorichi.com"]

def is_forbidden(uri):
    '''
    Checks if the requested URI matches any of the forbidden sites.
    Parameters:
        uri: The requested URI string to check.

    '''
    return any(site in uri for site in forbidden_sites)

def log_blocked_request(client_ip, uri):
    '''
    Logs any requests to forbidden sites to a file.
    
    Parameters:
        client_ip: The IP address of the client making the request.
        uri: The URI that was blocked.
        
    '''
    with open("blocked_requests_log.txt", "a") as log:
        log.write(f"Blocked Request from {client_ip} to URI: {uri}\n")

def handle_client(client_socket, client_address, server_ip, server_port):
    '''
    Manages client requests, checks if the request is to a forbidden URI, and either blocks it or forwards it to the server.
    
    Parameters:
        client_socket: The socket object for the client connection.
        client_address: The client's IP address and port.
        server_ip: IP address of the server.
        server_port: Port number of the server.
    
    '''
    request = client_socket.recv(BUFFER_SIZE).decode("utf-8")
    print(f"Received request:\n{request}")

    if request.startswith("GET"):
        uri = request.split(" ")[1]

        if is_forbidden(uri):
            print(f"Blocking forbidden URI: {uri}")
            log_blocked_request(client_address[0], uri)
            forbidden_response = "HTTP/1.1 403 Forbidden\n\nAccess Denied".encode("utf-8")
            client_socket.sendall(forbidden_response)
        else:
            # Relay the request to the actual server
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((server_ip, server_port))
            server_socket.send(request.encode("utf-8"))

            # Get server response
            response = server_socket.recv(BUFFER_SIZE)
            server_socket.close()

            # Send the response back to the client
            client_socket.sendall(response)

    client_socket.close()

def run_censor_relay(relay_port=5557, server_ip='localhost', server_port=12345):
    '''
    Runs the censor relay server, listening on a specified port for incoming connections and starting threads to handle each connection.

    Parameters:
        relay_port: The port on which the censor relay listens.
        server_ip: IP address of the server to forward requests to.
        server_port: Port number of the server.

    '''
    relay_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relay_socket.bind(('', relay_port))
    relay_socket.listen(5)
    print(f"Censor Relay listening on port {relay_port}...")

    while True:
        client_socket, client_address = relay_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address, server_ip, server_port)).start()

if __name__ == "__main__":
    run_censor_relay()
