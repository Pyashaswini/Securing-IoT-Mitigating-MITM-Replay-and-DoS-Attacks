import socket

def client_program():
    host = ''  # IP address of the server Raspberry Pi
    port = 5000  # same port as the server

    client_socket = socket.socket()
    client_socket.connect((host, port))

    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    credentials = f"{username},{password}"
    client_socket.send(credentials.encode())
    
    # Receive the server's response (either file or error message)
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
