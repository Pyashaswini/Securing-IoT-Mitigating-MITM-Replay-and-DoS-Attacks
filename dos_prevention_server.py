import socket
import time
from collections import defaultdict
import logging

# Dictionary to track the number of connections per IP
connection_times = defaultdict(list)

# Time window and max connections allowed from the same IP
TIME_WINDOW = 10
MAX_CONNECTIONS = 10  # Allow only 10 connections from the same IP in 10 seconds

# Setting up logging
logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def rate_limiter(ip):
    current_time = time.time()

    # Filter out connections that are older than TIME_WINDOW
    connection_times[ip] = [t for t in connection_times[ip] if current_time - t < TIME_WINDOW]

    # If connections exceed the allowed threshold, deny the connection
    if len(connection_times[ip]) >= MAX_CONNECTIONS:
        return False

    # Otherwise, log the time of the connection
    connection_times[ip].append(current_time)
    return True

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(5)
   
    print("Server is listening for connections...")

    while True:
        try:
            conn, addr = server_socket.accept()
            ip_address = addr[0]

            # Implement rate limiting based on the IP
            if not rate_limiter(ip_address):
                print(f"Too many connections from {ip_address}, blocking!")
                logging.warning(f"Too many connections from {ip_address}, blocking!")
                conn.close()
                continue

            print(f"Connection accepted from {ip_address}")
            logging.info(f"Connection accepted from {ip_address}")
            
            data = conn.recv(1024)
            if not data:
                print(f"Connection from {ip_address} closed with no data received.")
                logging.info(f"Connection from {ip_address} closed with no data received.")
                conn.close()
                continue

            print(f"Received: {data.decode()}")
            conn.send("Message received.".encode())
            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"An error occurred: {e}")
            conn.close()

if __name__ == "__main__":
    server_program()
