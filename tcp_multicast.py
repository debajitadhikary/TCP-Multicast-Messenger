import socket
import threading

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555

# Function to handle each client connection
def handle_client(client_socket, client_address):
    print(f"Connection from {client_address}")
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received from {client_address}: {data.decode('utf-8')}")

            # Echo the received data back to the client
            client_socket.sendall(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Main function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            # Accept client connections
            client_socket, client_address = server_socket.accept()

            # Start a new thread to handle each client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()

# Client function to connect to the server
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to server {SERVER_HOST}:{SERVER_PORT}")

        while True:
            # Send data to the server
            message = input("Enter message to send: ")
            client_socket.sendall(message.encode('utf-8'))

            # Receive response from the server
            response = client_socket.recv(1024)
            print(f"Server response: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Start the client
    start_client()


