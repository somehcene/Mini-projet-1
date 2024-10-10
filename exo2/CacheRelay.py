import socket
import threading
import os

BUFFER_SIZE = 4096
cache = {}

def handle_client(client_socket, server_ip, server_port):
    request = client_socket.recv(BUFFER_SIZE).decode("utf-8")
    print(f"Received request:\n{request}")

    # Parse requested URI from HTTP GET
    if request.startswith("GET"):
        uri = request.split(" ")[1]
        if uri in cache:
            print(f"Serving from cache: {uri}")
            client_socket.sendall(cache[uri])
        else:
            print(f"Fetching from server for: {uri}")
            # Relay the request to the actual server
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((server_ip, server_port))
            server_socket.send(request.encode("utf-8"))

            # Get server response and store it in the cache
            response = server_socket.recv(BUFFER_SIZE)
            cache[uri] = response
            client_socket.sendall(response)
            server_socket.close()
    client_socket.close()

def run_cache_relay(relay_port=5555, server_ip='localhost', server_port=5556):
    relay_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relay_socket.bind(('', relay_port))
    relay_socket.listen(5)
    print(f"Cache Relay listening on port {relay_port}...")

    while True:
        client_socket, client_address = relay_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, server_ip, server_port)).start()

if __name__ == "__main__":
    run_cache_relay()
