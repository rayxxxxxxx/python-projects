from __future__ import annotations
import socket
import selectors

from src import ENCODING
import src.utils.networking as network


class ConnectionData:
    def __init__(self) -> None:
        self.messages: list[bytes] = list()


class Server:
    def __init__(self) -> None:
        self.sock: socket.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.connections: list[socket.socket] = list()
        self.selector: selectors.DefaultSelector = selectors.DefaultSelector()

    def setup(self, addr: tuple, max_conn: int) -> None:
        self.sock.setblocking(False)
        self.sock.bind(addr)
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
                for client, mask in events:
                    if not client.data:
                        accept_connection(self, client)
                    else:
                        serve_connection(self, client, mask)
            except KeyboardInterrupt:
                print(':::: KEYBOARD INTERRUPT ::::')
                self.shutdown()
                break

    def shutdown(self):
        for sock in self.connections:
            self.selector.unregister(sock)
            sock.close()

        self.connections.clear()
        self.selector.close()
        self.sock.close()


def accept_connection(server: Server, client: selectors.SelectorKey):
    conn, addr = client.fileobj.accept()
    conn.setblocking(False)

    server.connections.append(conn)
    server.selector.register(
        conn,
        selectors.EVENT_READ | selectors.EVENT_WRITE,
        data=ConnectionData()
    )

    print(f"{conn.getpeername()} has connected...")


def remove_connection(server: Server, conn: socket.socket):
    server.selector.unregister(conn)
    conn.close()
    server.connections.remove(conn)


def serve_connection(server: Server, client: selectors.SelectorKey, mask):
    if mask & selectors.EVENT_READ:
        handle_read_event(server, client)

    if mask & selectors.EVENT_WRITE:
        handle_write_event(server, client)


def handle_read_event(server: Server, client: selectors.SelectorKey):
    conn: socket.socket = client.fileobj
    conndata: conndata = client.data

    data = network.recvbytes(conn)

    if not data or data == b'\r\0':
        print(f"{conn.getpeername()} has disconnected...")
        remove_connection(server, conn)
    else:
        conndata.messages.append(data)
        print(f"{conn.getpeername()} {data.decode(ENCODING)}")


def handle_write_event(server: Server, client: selectors.SelectorKey):
    conn: socket.socket = client.fileobj
    conndata: conndata = client.data

    if conndata.messages:
        msg = conndata.messages.pop(0)
        for other_conn in server.connections:
            if other_conn != conn:
                network.sendbytes(other_conn, msg)
