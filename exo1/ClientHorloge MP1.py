import socket
import datetime
import random
import time

BUFFER_SIZE = 4096

def run_client(server_ip='localhost', server_port=5555, request_count=int(input("What's the request count? "))):
    '''
    Connects to the relay server, sends multiple requests asking for the current time, and calculates the round-trip time for each request.
    Parameters:
        server_ip: IP address of the relay server (default: 'localhost').
        server_port: Port number of the relay server (default: 5555).
        request_count: The number of requests to send to the server (prompted from the user).
    '''
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    print(f"Connected to server {server_ip}:{server_port}")

    # Send the request count to the server (as a 4-byte integer)
    client_socket.send(request_count.to_bytes(4, byteorder='big'))
    print(f"Sent request count: {request_count}")

    time_differences = []

    for i in range(request_count):
        time.sleep(random.uniform(0.5, 2))  # Simulate realistic delays

        # Send request to the server
        time_sent = datetime.datetime.now().isoformat()
        client_socket.send("what time is it?".encode('utf-8'))
        print(f"Sent request {i+1}: {time_sent}")

        # Receive server's time response
        server_time = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        time_received = datetime.datetime.now().isoformat()

        # Compute time difference
        time_difference = datetime.datetime.fromisoformat(time_received) - datetime.datetime.fromisoformat(time_sent)
        time_differences.append(time_difference)

        print(f"Request {i+1}: sent at {time_sent}, received at {time_received}")
        print(f"Server time: {server_time}, Time difference: {time_difference}")

    client_socket.close()
    return time_differences

if __name__ == '__main__':
    run_client()