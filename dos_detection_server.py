import socket
import logging
from collections import defaultdict
import time
import threading

# Setup logging to track incoming connections
logging.basicConfig(filename="server_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Dictionary to track the number of connections per IP
connections_per_ip = defaultdict(list)

# Time window to monitor connections (in seconds)
TIME_WINDOW = 10

# Threshold for number of connections allowed per IP within the time window
CONNECTION_THRESHOLD = 5  # Set lower for testing purposes

# Lock to prevent race conditions in multithreading
lock = threading.Lock()

def detect_dos_attack(ip):
    current_time = time.time()

    with lock:
        # Add the current time of the new connection
        connections_per_ip[ip].append(current_time)

        # Debugging: Print all connection times for the IP
        #print(f"All connection times for {ip}: {connections_per_ip[ip]}")

        # Filter out any connections that occurred outside the time window
        connections_per_ip[ip] = [t for t in connections_per_ip[ip] if current_time - t < TIME_WINDOW]

        # Debugging: Print the remaining valid connections for the IP
        #print(f"Valid connections for {ip} within {TIME_WINDOW} seconds: {connections_per_ip[ip]}")

        # If the number of valid connections exceeds the threshold, log the DoS attack
        if len(connections_per_ip[ip]) > CONNECTION_THRESHOLD:
            logging.warning(f"Possible DoS attack detected from IP: {ip}")
            print(f"DoS attack detected from {ip}!")
        else:
            print(f"Connection from {ip} is under the threshold.")

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    # Enable SO_REUSEADDR option to allow reuse of the address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   
    server_socket.bind(('0.0.0.0',5000))  # Bind to localhost on port 12345
    server_socket.listen(5)  # Listen for up to 5 connections
   
    print("Server is listening for connections...")

    while True:
        try:
            conn, addr = server_socket.accept()  # Accept an incoming connection
            ip_address = addr[0]
            print(f"Connection received from {ip_address}")
           
            # Detect potential DoS attack
            detect_dos_attack(ip_address)
           
            data = conn.recv(1024)  # Receive data from the client
            print(f"Received: {data.decode()}")
            conn.send("Message received.".encode())

        except BrokenPipeError:
            print(f"BrokenPipeError: Connection with {ip_address} was interrupted.")
            logging.error(f"BrokenPipeError: Connection with {ip_address} was interrupted.")

        except ConnectionResetError:
            print(f"ConnectionResetError: Connection with {ip_address} was reset.")
            logging.error(f"ConnectionResetError: Connection with {ip_address} was reset.")

        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"An error occurred with {ip_address}: {e}")

        finally:
            conn.close()  # Ensure the connection is closed after each interaction

if __name__ == "__main__":
    server_program()
