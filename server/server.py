import socket
import threading

clients = []  # List of connected clients

def broadcast(message, client_socket):
    """Sends a message to all other clients except the sender"""
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket, client_address):
    print(f"Connected to {client_address}")
    clients.append(client_socket)

    # Receive and send messages in a loop
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:  # If no message is received (client closes connection)
                break
            print(f"Received message from {client_address}: {message}")
            # Broadcast the message to all other clients
            broadcast(message, client_socket)
        except:
            break

    # Remove the client from the list if the connection is lost
    clients.remove(client_socket)
    client_socket.close()

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))  # Listen on port 12345
server.listen(5)

print("Waiting for connections...")
while True:
    client_socket, client_address = server.accept()
    # Use threading so the server can handle multiple clients at once
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
