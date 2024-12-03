import socket
import os

def server_program():
    host = '0.0.0.0'  # accept any incoming connection
    port = 5000  # arbitrary port

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))

    server_socket.listen(2)
    print("Server listening on port", port)

    while True:
        conn, address = server_socket.accept()
        print(f"Connection from {address} has been established.")
        
        # Receive the credentials from the client
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Received credentials: {data}")
        
        username, password = data.split(",")  # Assuming credentials are sent as 'username,password'
        
        # Check credentials against the file and retrieve patient file path
        patient_file_path = check_credentials(username, password)
        if patient_file_path:
            # If valid, send the patient's file(s) to the client
            send_patient_files(conn, patient_file_path)
        else:
            # If invalid, send error message
            conn.send("Invalid credentials.".encode())

        conn.close()

def check_credentials(username, password):
    # Read the credentials from a file (e.g., credentials.txt)
    try:
        with open("credentials.txt", "r") as file:
            credentials = file.readlines()
            for line in credentials:
                stored_username, stored_password, patient_files_path = line.strip().split(",")
                if stored_username == username and stored_password == password:
                    return patient_files_path  # Return the patient's file path if credentials are valid
    except FileNotFoundError:
        print("Credentials file not found!")
    return None  # Return None if no match found

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

if __name__ == '__main__':
    server_program()
