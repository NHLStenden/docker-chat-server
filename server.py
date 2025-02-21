import socket

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))  # Luistert op poort 12345
server.listen(1)

print("Wachten op verbinding...")
client, address = server.accept()
print(f"Verbonden met {address}")

# Ontvang en stuur berichten
while True:
    message = client.recv(1024).decode('utf-8')
    if message.lower() == 'exit':
        print("Verbonden afgesloten.")
        break
    print(f"Ontvangen bericht: {message}")
    response = input("Reageer: ")
    client.send(response.encode('utf-8'))

client.close()
server.close()

