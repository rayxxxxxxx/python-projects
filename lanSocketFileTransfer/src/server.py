import socket
import threading
from pathlib import Path
import configparser

conf = configparser.ConfigParser()
conf.read(Path('conf.ini'))

HEADER_SIZE = int(conf['SERVER']['HEADER_SIZE'])
ENCODING = conf['SERVER']['ENCODING']


def next_chunk(client_socket: socket.socket) -> tuple:
    data = client_socket.recv(HEADER_SIZE)
    
    if not data:
        return (b"", 0)
    
    chunk_size = int(data.decode(ENCODING).strip())
    
    return (client_socket.recv(chunk_size), chunk_size)


def receive_file(client_socket: socket.socket, file_size: int, file_name: str) -> int:
    bytes_received = 0    
    
    with open(Path(conf['APP']['DOWNLOAD_DIR'], file_name), 'wb') as file:
        while bytes_received < file_size:
            chunk, chunk_size = next_chunk(client_socket)
            bytes_received += chunk_size
            file.write(chunk)


def serve_client(client_socket: socket.socket, addr: str) -> None:    
    while True:
        chunk, chunk_size = next_chunk(client_socket)
        
        if chunk_size == 0 or chunk == b"\r\0":
            break

        chunk = chunk.decode(ENCODING).split("\t")
        file_size = int(chunk[0])
        file_name = chunk[1]
        
        receive_file(client_socket, file_size, file_name)        

    client_socket.close()


class Server:
    def __init__(self, host, port) -> None:
        self.host: str = host
        self.port: int = port

        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockets: list[socket.socket] = list()
        self.clients_threads: list[threading.Thread] = list()

    def run(self) -> None:
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)

        print(f'[SERVER] listening on: {self.host}:{self.port}')

        while True:
            try:
                client_socket, addr = self.sock.accept()
                
                new_client_thread = threading.Thread(
                    target=serve_client,
                    args=(client_socket, addr)
                )

                self.client_sockets.append(client_socket)
                self.clients_threads.append(new_client_thread)
                
                new_client_thread.start()
            except KeyboardInterrupt:
                self.client_sockets.clear()
                self.clients_threads.clear()
                self.sock.close()
                break

    def close(self) -> None:
        self.client_sockets.clear()
        self.clients_threads.clear()
        self.sock.close()


def main():
    HOST = conf['SERVER']['HOST']
    PORT = int(conf['SERVER']['PORT'])
    
    server = Server(HOST, PORT)
    server.run()


if __name__ == '__main__':
    main()
