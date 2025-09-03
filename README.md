# Python Audio File Transfer

This project is a simple audio file transfer system using **Python sockets** and **selectors** to enable efficient handling of multiple clients without using threading.  
Clients can connect to the server and upload an `.mp3` file, which the server receives and stores on disk.

---

## Features

- Handles multiple simultaneous client connections using `selectors`
- Each client can upload one `.mp3` file
- Files are saved with unique names based on connection order (e.g. `archivo_usuario0.mp3`)
- Uses `TCP` sockets with manual buffering
- Confirmation messages sent for each block received

---

## Server Behavior

- Listens on `localhost:65432`
- Accepts incoming client connections
- For each client:
  - Creates a unique ID based on their connection order
  - Receives and stores chunks of the file in memory
  - Once the client finishes sending, the server saves the file to disk in the path `./`

---

## Client Behavior

- Connects to the server via TCP
- Opens a local `.mp3` file (e.g. `song.mp3`)
- Sends the file in 1024-byte chunks
- Waits for a confirmation from the server after each chunk
- After the file is fully sent, it notifies the server with the message: `Archivo de audio enviado`

## How to Run

```bash
python Servidor.py
python Cliente.py
