import socket
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Shared secret key (must match the key used in client)
SECRET_KEY = b'16-byte-long-key'  # 16-byte key for AES-128

# Function to decrypt data using AES
def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:16]  # Extract the IV from the first 16 bytes
    encrypted_message = encrypted_data[16:]  # Get the actual encrypted data

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_message) + decryptor.finalize()

    # Remove padding
    pad_length = ord(decrypted_data[-1:])
    return decrypted_data[:-pad_length].decode()

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

        # Receive encrypted username and password
        encrypted_data = conn.recv(1024)

        # Split the data into encrypted username and password
        encrypted_username = encrypted_data[:32]  # First 32 bytes for username
        encrypted_password = encrypted_data[32:]  # Remaining bytes for password

        # Decrypt the username and password
        try:
            username = decrypt_data(encrypted_username, SECRET_KEY)
            password = decrypt_data(encrypted_password, SECRET_KEY)
            print(f"Decrypted credentials: {username}, {password}")
        except Exception as e:
            print(f"Decryption error: {e}")
            conn.send("Invalid credentials.".encode())
            conn.close()
            continue

        # Authenticate user
        patient_files_path = authenticate_user(username, password)
        if patient_files_path:
            print(f"Authentication successful for {username}")
            # Send the patient files (not implemented in this snippet)
            send_patient_files(conn, patient_files_path)
        else:
            print(f"Invalid credentials for {username}")
            conn.send("Invalid credentials.".encode())

        conn.close()

if __name__ == "__main__":
    server_program()
