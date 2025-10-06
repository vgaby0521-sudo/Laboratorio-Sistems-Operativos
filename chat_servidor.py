import socket
import threading

HOST = "localhost"
PORT = 6000
clientes = []
usuarios = {
    "Juan": "1234",
    "Valentina": "5678",
    "Osnaider": "abcd",
    "Gabriela": "efgh",
    "Hary": "ijkl"
}
lock = threading.Lock()

def autenticar(c):
    c.send(b"Usuario: ")
    user = c.recv(1024).decode().strip()
    c.send(b"Contrasena: ")
    pwd = c.recv(1024).decode().strip()

    if usuarios.get(user) == pwd:
        c.send(f"Bienvenido {user}\n".encode())
        return user
    else:
        c.send(b"Usuario o contrasena incorrectos\n")
        return None

def enviar_todos(msg, origen, es_binario=False):
    with lock:
        for cliente in clientes:
            if cliente != origen:
                try:
                    if es_binario:
                        cliente.sendall(msg)
                    else:
                        cliente.sendall(msg.encode())
                except:
                    pass

def atender(c, addr, user):
    print(user, "se conectó desde", addr)
    try:
        while True:
            data = c.recv(4096)
            if not data:
                break

            try:
                texto = data.decode().strip()
            except:
                texto = None

            if texto and not texto.startswith("FILE:"):
                print(user + ":", texto)
                with open("chat_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"{user}: {texto}\n")
                enviar_todos(f"{user}: {texto}", c)

            elif texto and texto.startswith("FILE:"):
                partes = texto.split(":")
                nombre = partes[1]
                tamaño = int(partes[2])

                print(f"{user} está enviando archivo: {nombre} ({tamaño} bytes)")

                with open("chat_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"{user} envió archivo: {nombre} ({tamaño} bytes)\n")

                enviar_todos(f"{user} está enviando archivo: {nombre}", c)
                enviar_todos(f"FILE:{nombre}:{tamaño}\n", c)

                recibido = 0
                while recibido < tamaño:
                    bloque = c.recv(4096)
                    if not bloque:
                        break
                    recibido += len(bloque)
                    enviar_todos(bloque, c, es_binario=True)

                print("Archivo reenviado:", nombre)

    except Exception as e:
        print("Error:", e)
    finally:
        with lock:
            if c in clientes:
                clientes.remove(c)
        c.close()
        print(user, "se desconectó")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print("Servidor de chat en", HOST, "puerto", PORT)

    while True:
        c, addr = s.accept()
        user = autenticar(c)
        if user:
            with lock:
                clientes.append(c)
            hilo = threading.Thread(target=atender, args=(c, addr, user))
            hilo.start()
        else:
            c.close()

if __name__ == "__main__":
    main()
