import socket

HOST = "127.0.0.1"
PORT = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen()
print(f"Server listening on {HOST}:{PORT}\n")

conn, addr = server.accept()
print(f"Connected by {addr}\n")

while True:
    conn.sendall(b"--> ")
    data = conn.recv(1024)

    message = data.decode().strip()
    print("Received:", message)
    
    exitCodes= ["quit", "bye", "close"]

    if message in exitCodes: 
        conn.sendall(b"Goodbye!\n")
        conn.close()
        break
    else:
        conn.sendall(b"Hello from Python server!\n")


