import socket
import selectors   
import socket

HOST = "localhost"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432 # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024
users = [] #registro de usuarios conectados
song = [] #Será el registro donde se guardarán las canciones de cada uno de los usuarios conectados
sel = selectors.DefaultSelector()

def accept(sock_a, mask):
    sock_conn, addr = sock_a.accept()  
    print('Conección aceptada', sock_conn, ' direccion:', addr)
    users.append(sock_conn) #Se agrega la coneccion del usuario al registro de usuarios
    sock_conn.setblocking(False)
    if len(song) < len(users): #Se verifica que la longitud de song y users sea del mismo tamaño
        song.append([]) #En caso de no ser del mismo tamaño se agrega un apartado para agregar una lista en song
    print("Usuarios que se han conectado : ",len(users)) #Nos muestra el número de usuarios que se han conectado
    print(users)
    print("Canciones guardadas:  ", len(song),"\n") #Nos muestra el número de canciones guardadas
    sel.register(sock_conn, selectors.EVENT_READ, read)#Se registra en el selector el socket del cliente con el evento de lectura y con la funcion read

def read(sock_c, mask):
    numero = str(users.index(sock_c)) #indice que tiene cada usuario, lo usamos como tipo id, para guardar las canciones en esa posición en song
    if mask & selectors.EVENT_READ:
        data = sock_c.recv(buffer_size)  # Se reciben los bytes en bloques de 1024
        if 'Archivo de audio enviado' in str(data) :
            print("Envío terminado, cerrando conexión", sock_c)
            direccion = "./archivo_usuario"+numero+".mp3"
            print("Id que le correspondió a este cliente:  ",numero," \nDireccion donde se guardo el archivo: ",direccion,"\n")
            with open (direccion, "wb") as cancion:
                for i in song[int(numero)]:
                    cancion.write(i)
            sel.unregister(sock_c)
            sock_c.close()
        elif data:
            #print('recibido', data, 'a', sock_c) #Solo se recibe el archivo mp3
            sock_c.sendall(b'Recibido con exito')
            #numero = str(users.index(sock_c))
            song[int(numero)].append(data)
            #print(song)
with socket.socket() as Serveraccept:
    Serveraccept.bind((HOST, PORT))
    Serveraccept.listen(100)
    Serveraccept.setblocking(False)
    print("Inicializando servidor...")
    sel.register(Serveraccept, selectors.EVENT_READ, accept)
    while True:
        #print("Esperando eventos...")
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
