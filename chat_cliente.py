import socket
import threading
import os

HOST = "localhost"
PORT = 6000

def escuchar(sock):
    buffer = b""
    while True:
        try:
            datos = sock.recv(4096)
            if not datos:
                break
            buffer += datos

            while b"\n" in buffer:
                linea, buffer = buffer.split(b"\n", 1)
                try:
                    texto = linea.decode().strip()
                except UnicodeDecodeError:
                    continue

                if texto.startswith("FILE:"):
                    partes = texto.split(":")
                    nombre = partes[1]
                    tamaño = int(partes[2])
                    guardar = "recibido_" + nombre
                    print(f"\nRecibiendo archivo: {guardar} ({tamaño} bytes)")

                    recibido = 0
                    with open(guardar, "wb") as f:
                        while recibido < tamaño:
                            bloque = sock.recv(4096)
                            if not bloque:
                                break
                            f.write(bloque)
                            recibido += len(bloque)

                    print("Archivo recibido:", guardar)
                else:
                    print(texto)

        except:
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    datos = s.recv(1024).decode()
    print(datos, end="")
    user = input()
    s.sendall(user.encode() + b"\n")

    datos = s.recv(1024).decode()
    print(datos, end="")
    pwd = input()
    s.sendall(pwd.encode() + b"\n")

    datos = s.recv(1024).decode()
    print(datos, end="")

    if "incorrectos" in datos:
        s.close()
    else:
        threading.Thread(target=escuchar, args=(s,), daemon=True).start()

        while True:
            msg = input()
            if msg.lower() == "salir":
                break

            if msg.startswith("/enviar "):
                nombre = msg.split(" ", 1)[1]
                if os.path.exists(nombre):
                    tamaño = os.path.getsize(nombre)
                    s.sendall(f"FILE:{nombre}:{tamaño}\n".encode())
                    with open(nombre, "rb") as f:
                        while True:
                            bloque = f.read(4096)
                            if not bloque:
                                break
                            s.sendall(bloque)
                    print("Archivo enviado:", nombre)
                else:
                    print("No existe el archivo:", nombre)
            else:
                s.sendall(msg.encode())
