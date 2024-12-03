import socket
import os
# List of allowed IP addresses (stored server-side)
ALLOWED_IPS = ['', '']  # Add allowed IPs

# Function to authenticate user
def authenticate_user(username, password):
    try:
        # Reading the credentials from a file (for example: credentials.txt)
        with open('credentials.txt', 'r') as file:
            credentials = file.readlines()
            for line in credentials:
                stored_username, stored_password, patient_files_path = line.strip().split(',')
                if stored_username == username and stored_password == password:
                    return patient_files_path  # Return the directory of patient files if valid
    except FileNotFoundError:
        print("Credentials file not found.")
    return None  # Invalid credentials
    
def send_patient_files(conn, file_path):
    # Check if the path is a directory or a specific file and send accordingly
    if os.path.isdir(file_path):
        # If it's a directory, send all files in the directory
        for filename in os.listdir(file_path):
            full_file_path = os.path.join(file_path, filename)
            if os.path.isfile(full_file_path):
                send_file(conn, full_file_path)
    elif os.path.isfile(file_path):
        # If it's a single file, send that file
        send_file(conn, file_path)
    else:
        conn.send("No valid patient files found.".encode())

def send_file(conn, file_path):
    with open(file_path, "rb") as file:
        file_data = file.read()
        conn.send(file_data)  # Send the file's content to the client
        print(f"Sent file {file_path}")

# Server program
def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(5)

    print("Server is listening for connections...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection accepted from {addr}")

        # Extract the client's IP address from the connection
        client_ip = addr[0]

        # Check if the client's IP address is allowed
        if client_ip not in ALLOWED_IPS:
            print(f"Warning: Possible MITM attack! Untrusted IP address: {client_ip}")
            

        # Receive data (username + password in plaintext)
        data = conn.recv(1024)
        
        # Check if data is empty or not enough for the username/password split
        if not data or b',' not in data:
            print("Error: Invalid data format received from client.")
            conn.send("Invalid data format.".encode())
            conn.close()
            continue
        
        # Split the data into username and password
        username, password = data.split(b',', 1)

        # Authenticate user
        patient_files_path = authenticate_user(username.decode(), password.decode())
        if patient_files_path:
            print(f"Authentication successful for {username.decode()}")
            # Send the patient files (not implemented in this snippet)
            send_patient_files(conn, patient_files_path)
        else:
            print(f"Invalid credentials for {username.decode()}")
            conn.send("Invalid credentials.".encode())

        conn.close()

if __name__ == "__main__":
    server_program()
