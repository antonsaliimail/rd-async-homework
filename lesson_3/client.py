import socket

so = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

so.connect(("localhost", 8000))  # Blocking
print("Connected")

while True:
    msg_bytes = so.recv(1024)  # Blocking

    message = msg_bytes.decode()

    print(f"Received weather data: {message}")

    if message == "exit":
        break

so.close()
