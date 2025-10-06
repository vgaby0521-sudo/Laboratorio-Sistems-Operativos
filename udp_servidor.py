import socket

HOST = "localhost"
PORT = 7000
BUFFER = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
print("Servidor UDP en", HOST, PORT)

while True:
    datos, addr = s.recvfrom(BUFFER)
    print("Mensaje de", addr, ":", datos.decode())
    respuesta = "ECO: " + datos.decode()
    s.sendto(respuesta.encode(), addr)
