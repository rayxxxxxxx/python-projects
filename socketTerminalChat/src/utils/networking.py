import socket

from utils import ENCODING, HEADER_SIZE
from utils.data_prepocessing import add_header


def sendbytes(sock: socket.socket, data: bytes) -> None:
    prepared = add_header(data)
    sock.sendall(prepared)


def sendstr(sock: socket.socket, data: str) -> None:
    prepared = add_header(data.encode(ENCODING))
    sock.sendall(prepared)


def recvbytes(sock: socket.socket) -> bytes:
    header = sock.recv(HEADER_SIZE)

    if header:
        dsize = int(header.decode(ENCODING).strip())
        data = sock.recv(dsize)
        return data

    return b''


def recvstr(sock: socket.socket) -> str:
    header = sock.recv(HEADER_SIZE)

    if header:
        dsize = int(header.decode(ENCODING).strip())
        data = sock.recv(dsize).decode(ENCODING)
        return data

    return ''
