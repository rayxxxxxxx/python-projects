import socket
from datetime import datetime

from utils import *


def timed(text):
    return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}"


def main():
    hostname = socket.gethostname()

    host = socket.gethostbyname(hostname)
    port = 9999
    server_address = (host, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen(1)
    print(timed("SERVER IS UP"))

    conn, addr = sock.accept()
    print(timed(f"{addr[0]}:{addr[1]} HAS CONNECTED"))

    while True:
        try:
            data = recv_data(conn)

            if not data:
                conn.close()
                sock.close()
                break

            text = data.decode(ENCODING)
            print(timed(f"({addr[0]}:{addr[1]}) ({len(data)} bytes) {text}"))

            send_data(conn, text)

        except KeyboardInterrupt:
            conn.close()
            sock.close()
            break

    print(timed("SERVER IS DOWN"))


if __name__ == '__main__':
    main()
