import socket
import threading

BUFFER_SIZE = 4096

def handle_client(client_socket, server_ip, server_port):
    '''
    Relays client requests to the server and forwards the server's response back to the client.
    Parameters:
        client_socket: The socket object for the client connection.
        server_ip: IP address of the server to forward the requests to.
        server_port: Port number of the server.
    '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_ip, server_port))

    try:
        # Recevoir le nombre de requêtes
        count_data = client_socket.recv(4)
        server_socket.sendall(count_data)

        request_count = int.from_bytes(count_data, byteorder='big')

        for _ in range(request_count):
            client_message = client_socket.recv(BUFFER_SIZE)
            server_socket.sendall(client_message)

            # Recevoir la réponse du serveur et l'envoyer au client
            server_response = server_socket.recv(BUFFER_SIZE)
            client_socket.sendall(server_response)

    finally:
        client_socket.close()
        server_socket.close()

def run_relay(relay_port=5555, server_ip='localhost', server_port=1236):
    '''
    Starts the relay server, listens for incoming client connections, and spawns threads to relay requests between the client and the server.
    Parameters:
        relay_port: The port on which the relay listens for connections.
        server_ip: The IP address of the upstream server.
        server_port: The port number of the upstream server.
        
    '''
    relay_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relay_socket.bind(('', relay_port))
    relay_socket.listen(5)
    print(f"Relay listening on port {relay_port}...")

    while True:
        client_socket, addr = relay_socket.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket, server_ip, server_port)).start()

if __name__ == '__main__':
    run_relay()





