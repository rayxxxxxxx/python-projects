from __future__ import annotations
from pathlib import Path
import socket
import selectors
import configparser
from datetime import datetime

import utils.socket_utils as sockutil
from modules.data_token import DataToken
from modules.socket_data import SocketData
from modules.message import Message

conf = configparser.ConfigParser()
conf.read(Path('config.conf'))

ENCODING = conf.get('SYSTEM', 'ENCODING')
HEADER_SIZE = int(conf.get('SYSTEM', 'HEADER_SIZE'))
BUFFER_SIZE = int(conf.get('SYSTEM', 'BUFFER_SIZE'))


class ChatServer:
    def __init__(self) -> None:
        self.sock: socket.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.clients: list[socket.socket] = list()
        self.selector: selectors.DefaultSelector = selectors.DefaultSelector()

    def setup(self, addr: tuple, max_conn: int) -> None:
        self.sock.bind(addr)
        self.sock.setblocking(False)
        self.sock.listen(max_conn)

        self.selector.register(
            self.sock,
            selectors.EVENT_READ,
            data=None
        )

        print(f"[SERVER] ready...")

    def mainloop(self):
        while True:
            try:
                events = self.selector.select(timeout=None)
                for key, mask in events:
                    if not key.data:
                        accept_connection(self, key)
                    else:
                        serve_connection(self, key, mask)
            except KeyboardInterrupt:
                print(':::: KEYBOARD INTERRUPT ::::')
                self.shutdown()
                break

    def shutdown(self):
        for sock in self.clients:
            self.selector.unregister(sock)
            sock.close()

        self.clients.clear()
        self.selector.close()
        self.sock.close()


def accept_connection(server: ChatServer, key: selectors.SelectorKey):
    conn, addr = key.fileobj.accept()
    conn.setblocking(False)

    server.clients.append(conn)
    server.selector.register(
        conn,
        selectors.EVENT_READ | selectors.EVENT_WRITE,
        data=SocketData()
    )

    print(f"{conn.getpeername()} has connected...")


def remove_connection(server: ChatServer, sock: socket.socket):
    server.selector.unregister(sock)
    sock.close()
    server.clients.remove(sock)


def serve_connection(server: ChatServer, key: selectors.SelectorKey, mask):
    if mask & selectors.EVENT_READ:
        handle_read_event(server, key)

    if mask & selectors.EVENT_WRITE:
        handle_write_event(server, key)


def handle_read_event(server: ChatServer, key: selectors.SelectorKey):
    sock: socket.socket = key.fileobj
    sockdata: SocketData = key.data

    data = sockutil.recvbytes(sock)

    if not data or data == DataToken.DISCONNECT.value:
        print(f"{sock.getpeername()} has disconnected...")
        remove_connection(server, sock)
    else:
        sockdata.messages.append(Message(data))
        print(f"{sock.getpeername()} {data.decode(ENCODING)}")


def handle_write_event(server: ChatServer, key: selectors.SelectorKey):
    sock: socket.socket = key.fileobj
    sockdata: SocketData = key.data

    if sockdata.messages:
        msg = sockdata.messages.pop(0)
        for other_sock in server.clients:
            if other_sock != sock:
                msg.addmeta(f"[{datetime.today()}]")
                other_sock.sendall(msg.prepare())


def main():
    HOST = conf.get('SERVER', 'HOST')
    PORT = int(conf.get('SERVER', 'PORT'))

    server = ChatServer()
    server.setup((HOST, PORT), 10)
    server.mainloop()


if __name__ == '__main__':
    main()
