import socket
import threading
import signal
import sys
import getopt

clients = []
clients_lock = threading.Lock()
shutdown_event = threading.Event()

def broadcast(message, sender_socket):
    """Stuur bericht naar alle clients behalve de afzender"""
    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    client.close()
                    clients.remove(client)

def handle_client(client_socket, client_address):
    print(f"📥 Client connected: {client_address}")
    with clients_lock:
        clients.append(client_socket)

    try:
        while not shutdown_event.is_set():
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"📨 From {client_address}: {message}")
            broadcast(message, client_socket)
    except:
        pass
    finally:
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)
        client_socket.close()
        print(f"❌ Client disconnected: {client_address}")

def shutdown_server(server_socket):
    print("\n🛑 Shutting down server...")
    shutdown_event.set()
    try:
        server_socket.close()
    except:
        pass
    with clients_lock:
        for client in clients:
            try:
                client.close()
            except:
                pass
    print("✅ Server shutdown complete.")
    sys.exit(0)

def main(argv):
    host = '0.0.0.0'
    port = 12345

    # Command-line opties verwerken
    try:
        opts, _ = getopt.getopt(argv, "i:p:", ["ip=", "port="])
    except getopt.GetoptError:
        print("Usage: python server.py [-i <ip>] [-p <port>]")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--ip"):
            host = arg
        elif opt in ("-p", "--port"):
            port = int(arg)

    # Socket setup
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)

    print(f"✅ Server listening on {host}:{port}")

    # Ctrl+C afvangen
    def signal_handler(sig, frame):
        shutdown_server(server)
    signal.signal(signal.SIGINT, signal_handler)

    while not shutdown_event.is_set():
        try:
            client_socket, client_address = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
        except OSError:
            break  # Server socket is gesloten

if __name__ == "__main__":
    main(sys.argv[1:])
