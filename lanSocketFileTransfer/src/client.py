import os
import socket
from pathlib import Path
import configparser

from modules.socket_token import SocketToken

conf = configparser.ConfigParser()
conf.read(Path('conf.ini'))

HEADER_SIZE = int(conf['SERVER']['HEADER_SIZE'])
BUFFER_SIZE = int(conf['SERVER']['BUFFER_SIZE'])
ENCODING = conf['SERVER']['ENCODING']


def add_size_header(data: bytes):
    size = len(data)
    size_header = str(size).encode()+b' '*(HEADER_SIZE-len(str(size)))
    return size_header+data


class Client:
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port) -> None:
        self.sock.connect((host, port))

    def disconnect(self) -> None:
        self.send_all_bytes(SocketToken.DISCONNECT.value)

    def send_all_bytes(self, data: bytes) -> None:
        self.sock.sendall(add_size_header(data))

    def send_all_text(self, text: str) -> None:
        self.sock.sendall(add_size_header(text.encode(ENCODING)))

    def send_file(self, file_path: Path) -> None:
        fsize = os.path.getsize(file_path)
        fname = os.path.basename(file_path)

        self.send_all_text(f"{fsize}\t{fname}")
        
        with open(file_path, 'rb') as file:
            data = file.read(BUFFER_SIZE-HEADER_SIZE)
            while data:
                self.send_all_bytes(data)
                data = file.read(BUFFER_SIZE-HEADER_SIZE)


def main():
    HOST = conf['SERVER']['HOST']
    PORT = int(conf['SERVER']['PORT'])

    client = Client()
    client.connect(HOST, PORT)

    fp = Path('data', 'cat_meme.webm')
    client.send_file(fp)
    client.disconnect()


if __name__ == '__main__':
    main()
