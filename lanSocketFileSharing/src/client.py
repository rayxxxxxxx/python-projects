import io
import os
import socket
from pathlib import Path
import configparser

from modules.socket_token import SokenToken
from modules.socket_header import SocketHeader

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
        header = SocketHeader()
        header.add('action', 'disconnect')
        self.sock.sendall(add_size_header(header.as_bytes()))
        self.sock.close()

    def sendall(self, data: bytes) -> None:
        self.sock.sendall(add_size_header(data))

    def send_text(self, text: str) -> None:
        self.sock.sendall(add_size_header(text.encode(ENCODING)))

    def send_file(self, file_path: Path) -> None:
        with io.open(file_path, 'rb') as file:
            data = file.read(BUFFER_SIZE)
            while data:
                self.sock.sendall(add_size_header(data))
                data = file.read(BUFFER_SIZE)


def main():
    HOST = conf['SERVER']['HOST']
    PORT = int(conf['SERVER']['PORT'])

    client = Client()

    client.connect(HOST, PORT)

    fname = 'cat.webm'
    fp = Path('data', fname)

    header = SocketHeader()
    header.add('action', 'download')
    header.add('data-type', 'file')
    header.add('file-name', fname)
    header.add('file-size', os.path.getsize(fp))

    client.sendall(header.as_bytes())

    client.send_file(fp)

    client.disconnect()


if __name__ == '__main__':
    main()
