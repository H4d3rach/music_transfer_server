import socket
HOST = "localhost"  # Hostname o  dirección IP del servidor
PORT = 65432  # Puerto del servidor
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Enviando mensaje...")
    with open("audio.mp3", "rb") as audio:
        while bytes_leidos := audio.read(buffer_size):
            TCPClientSocket.sendall(bytes_leidos)
            print(bytes_leidos)
            resp_server = TCPClientSocket.recv(buffer_size)
    TCPClientSocket.sendall(b'Archivo de audio enviado')
    print("Terminé")