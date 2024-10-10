from socket import *
from pathlib import Path
import threading

def handle_client(client_connection, client_address):
    print(f"Connected by {client_address}")

    # Receive the HTTP request from the client
    request = client_connection.recv(1024).decode("utf-8")
    print(f"Request:\n{request}")

    # Extract the requested file from the HTTP GET request
    if request.startswith("GET "): 
        try:
            http_response = f"""\
HTTP/1.1 200 OK

<html lang="fr">
<head><meta charset="UTF-8"><title>TME1 PROGRAMMATION RESEAUX SU</title></head>
<body><h1>The web server is working</h1></body>
</html> 
"""
        
        except Exception as e:
            http_response = f"""\
HTTP/1.1 500 Internal Server Error

<html>
<head><title>500 Internal Server Error</title></head>
<body><h1>500 Internal Server Error</h1><p>{str(e)}</p></body>
</html>
"""
    else: 
        http_response = "Server only responds to http requests"

    client_connection.sendall(http_response.encode("utf-8"))
    client_connection.close()

def run_server():
    portNumber = 12345
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', portNumber))
    serverSocket.listen(1)
    print(f"Server listening on port {portNumber}...")
   
    #webPages_dir = Path(__file__).parent / 'WebPages'

    while True:
        client_connection, client_address = serverSocket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_connection, client_address))
        client_thread.start()

if __name__ == "__main__":
    run_server()