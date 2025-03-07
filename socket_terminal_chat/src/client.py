import socket

import src.utils.networking as network


class Client:
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, addr: tuple) -> None:
        try:
            self.sock.connect(addr)
            self.sock.setblocking(False)
        except ConnectionRefusedError:
            self.sock.close()

    def disconnect(self) -> None:
        network.sendbytes(self.sock, b"\r\0")
        self.sock.close()

    def sendbytes(self, data: bytes) -> None:
        network.sendbytes(self.sock, data)

    def recvbytes(self) -> bytes:
        try:
            return network.recvbytes(self.sock)
        except BlockingIOError:
            return b''
