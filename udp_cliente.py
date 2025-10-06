import socket

HOST = "localhost"
PORT = 7000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        mensaje = input("Escribe mensaje o salir: ")
        if mensaje.lower() == "salir":
            break
        s.sendto(mensaje.encode(), (HOST, PORT))
        datos, _ = s.recvfrom(2048)
        print("Servidor respondió:", datos.decode())
