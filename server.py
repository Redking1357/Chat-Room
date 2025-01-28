import socket
import threading

# List to keep track of connected clients and their names
clients = []
client_names = {}

# Broadcast function to send messages to all clients
def broadcast(message, client):
    for c in clients:
        if c != client:
            try:
                c.send(message)
            except:
                clients.remove(c)

# Handle client communication
def handle_client(client):
    # Receive the client's name immediately after they connect
    name = client.recv(1024).decode()  # Get name from client
    client_names[client] = name

    # Inform other clients that a new user has joined
    broadcast(f"{name} has joined the chat!".encode(), client)

    while True:
        try:
            message = client.recv(1024)
            if message:
                # Prepend the name to the message before broadcasting
                broadcast(f"{name}: {message.decode()}".encode(), client)
            else:
                break
        except:
            break

    # Remove client from list and notify others when they disconnect
    clients.remove(client)
    del client_names[client]
    broadcast(f"{name} has left the chat.".encode(), client)

# Set up the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12345))  # Localhost, port 12345
    server.listen(5)
    print("Server is running... Waiting for clients to connect.")

    while True:
        client, address = server.accept()
        clients.append(client)
        print(f"New connection from {address}")
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    start_server()
