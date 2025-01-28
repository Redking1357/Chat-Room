import socket
import threading

# Function to receive messages from the server
def receive_message(client):
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("Connection to the server was lost.")
            break

# Function to send messages to the server
def send_message(client, name):
    while True:
        message = input(f"{name}: ")  # Show the name before the input prompt
        client.send(message.encode())  # Send the message content to the server

# Set up the client
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12345))  # Connect to server at localhost, port 12345

    # Ask the user for their name once
    name = input("Enter your name: ")
    client.send(name.encode())  # Send name to the server when connecting

    # Start the threads to receive and send messages
    receive_thread = threading.Thread(target=receive_message, args=(client,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_message, args=(client, name))
    send_thread.start()

if __name__ == "__main__":
    start_client()
