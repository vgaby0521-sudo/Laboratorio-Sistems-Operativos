import socket
import threading
import os

HOST = "localhost"
PORT = 7000
BUFFER = 4096

def manejar_cliente(conn, addr):
    print(f"Cliente conectado: {addr}")
    try:
        nombre = conn.recv(BUFFER).decode()
        if not nombre:
            return

        if os.path.exists(nombre):
            tamaño = os.path.getsize(nombre)
            conn.sendall(str(tamaño).encode())
            with open(nombre, "rb") as f:
                while (data := f.read(BUFFER)):
                    conn.sendall(data)
            print(f"Archivo '{nombre}' enviado a {addr}")
        else:
            conn.sendall(b"0")
            print(f"Archivo '{nombre}' no encontrado")

    except Exception as e:
        print("Error con el cliente:", e)
    finally:
        conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Servidor de archivos iniciado en {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
