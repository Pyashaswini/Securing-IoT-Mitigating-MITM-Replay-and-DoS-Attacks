import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Shared secret key (must be kept secure)
SECRET_KEY = b'16-byte-long-key'  # 16-byte key for AES-128

# Function to encrypt data using AES
def encrypt_data(data, key):
    iv = os.urandom(16)  # Generate a random initialization vector (IV)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Ensure the data is a multiple of 16 bytes (padding)
    pad_length = 16 - len(data) % 16
    padded_data = data + chr(pad_length) * pad_length

    encrypted_data = encryptor.update(padded_data.encode()) + encryptor.finalize()
    return iv + encrypted_data  # Prepend IV to encrypted data

# Client program
def client_program():
    host = ''  # Server IP address
    port = 5000  # Port number

    client_socket = socket.socket()
    client_socket.connect((host, port))

    # Collect username and password from user
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Encrypt the username and password
    encrypted_username = encrypt_data(username, SECRET_KEY)
    encrypted_password = encrypt_data(password, SECRET_KEY)

    # Send encrypted data to the server
    client_socket.send(encrypted_username + encrypted_password)

    # Receive server response (file or error message)
    data = client_socket.recv(1024)

    if data == b"Invalid credentials.":
        print("Authentication failed. Incorrect username or password.")
    else:
        # If files are sent, save them
        with open("received_patient_file", "wb") as file:
            file.write(data)
        print("File received successfully.")

    client_socket.close()

if __name__ == '__main__':
    client_program()
