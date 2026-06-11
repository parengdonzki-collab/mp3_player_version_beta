import socket
import random
import time

print("Connecting...")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 6000))

print("Connected!")

while True:
    bars = [str(random.random()) for _ in range(20)]
    data = ",".join(bars) + "\n"

    sock.send(data.encode())
    print("Sent:", data[:50])

    time.sleep(0.05)  