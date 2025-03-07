import socket
import selectors
from datetime import datetime

from utils import *


sel = selectors.DefaultSelector()


def timed(text: str) -> str:
    return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}"


def read_handler(sock: socket.socket, mask: int) -> None:
    addr = sock.getpeername()
    data = recv_data(sock)

    if not data:
        sel.unregister(sock)
        sock.close()
        print(timed(f"{addr[0]}:{addr[1]} HAS DISCONNECTED"))
        return

    text = data.decode(ENCODING)
    print(timed(f"({addr[0]}:{addr[1]}) {text}"))
    send_data(sock, text)


def accept_handler(sock: socket.socket, mask: int) -> None:
    conn, addr = sock.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read_handler)
    print(timed(f"{addr[0]}:{addr[1]} HAS CONNECTED"))


def main():
    hostname = socket.gethostname()
    host, port = socket.gethostbyname(hostname), 9999
    server_address = (host, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.bind(server_address)
    sock.listen(5)
    sel.register(sock, selectors.EVENT_READ, accept_handler)

    print(timed("SERVER IS UP"))

    while True:
        try:
            for key, mask in sel.select(timeout=1):
                conn, handler = key.fileobj, key.data
                handler(conn, mask)
        except KeyboardInterrupt:
            sel.close()
            sock.close()
            break

    print(timed("SERVER IS DOWN"))


if __name__ == '__main__':
    main()
