import socket
import threading

def listen_for_messages(client_socket):
    """Listens for messages from the server (from other clients)"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"Message from another client: {message}")
        except:
            print("Connection lost.")
            break

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('chat_server', 12345))  # Connect to the server via the 'chat_server' name (Docker Compose)

# Start a thread to listen for messages from other clients
thread = threading.Thread(target=listen_for_messages, args=(client,))
thread.start()

# Send messages to the server
while True:
    message = input("Your message: ")
    if message.lower() == 'exit':
        break
    client.send(message.encode('utf-8'))

client.close()
