import io
import socket
import threading
from pathlib import Path
import configparser

from modules.socket_token import SokenToken
from modules.socket_header import SocketHeader

conf = configparser.ConfigParser()
conf.read(Path('conf.ini'))

HEADER_SIZE = int(conf['SERVER']['HEADER_SIZE'])
ENCODING = conf['SERVER']['ENCODING']


def next_chunk(conn: socket.socket) -> bytes:
    data = conn.recv(HEADER_SIZE)
    if not data:
        return (b'', 0)
    chunk_size = int(data.decode(ENCODING).strip())
    return (conn.recv(chunk_size), chunk_size)


def receive_file(conn: socket.socket, file_size: int, file_name: str) -> int:
    buffer = io.BytesIO()
    bytes_received = 0
    while bytes_received < file_size:
        chunk, chunk_size = next_chunk(conn)
        buffer.write(chunk)
        bytes_received += chunk_size

    with open(Path(conf['APP']['SAVE_DIR'], file_name), 'wb') as file:
        file.write(buffer.getvalue())


def serve_client(server: socket.socket, conn: socket.socket, addr: str) -> None:
    connected = True
    while connected:
        chunk, chunk_size = next_chunk(conn)
        if chunk_size == 0:
            continue

        headers = SocketHeader.from_bytes(chunk)

        if headers['action'] == 'disconnect':
            connected = False
            print(f'disconnected {addr}')
            continue

        if headers['data-type'] == 'file':
            receive_file(conn, headers['file-size'], headers['file-name'])


class Server:
    def __init__(self, host, port) -> None:
        self.host: str = host
        self.port: int = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients_threads: list[threading.Thread] = list()

    def run(self) -> None:
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)

        print(f'--- server working on {self.host}:{self.port} ---')

        while True:
            try:
                conn, addr = self.sock.accept()
                print(f'new connection from {addr}')
                new_client_thread = threading.Thread(
                    target=serve_client,
                    args=(self.sock, conn, addr)
                )
                self.clients_threads.append(new_client_thread)
                new_client_thread.start()
            except KeyboardInterrupt:
                self.clients_threads.clear()
                self.sock.close()
                break

    def close(self) -> None:
        self.sock.close()


def main():
    HOST = conf['SERVER']['HOST']
    PORT = int(conf['SERVER']['PORT'])
    server = Server(HOST, PORT)
    server.run()


if __name__ == '__main__':
    main()
