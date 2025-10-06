import socket
import os

HOST = "localhost"
PORT = 7000
BUFFER = 4096

def solicitar_archivo(nombre):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(nombre.encode())

        tamaño = s.recv(BUFFER).decode()
        if tamaño == "0":
            print("El archivo no existe en el servidor.")
            return

        tamaño = int(tamaño)
        recibido = 0
        with open("descargado_" + nombre, "wb") as f:
            while recibido < tamaño:
                data = s.recv(BUFFER)
                if not data:
                    break
                f.write(data)
                recibido += len(data)

        print(f"Archivo '{nombre}' descargado correctamente.")

def main():
    nombre = input("Nombre del archivo a descargar: ")
    solicitar_archivo(nombre)

if __name__ == "__main__":
    main()
