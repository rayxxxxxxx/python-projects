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
    sock.connect(server_address)

    while True:
        try:
            text = input('> ')

            if text == '.exit':
                sock.close()
                break

            send_data(sock, text)
            data = recv_data(sock)

            if not data:
                sock.close()
                break

            text = data.decode(ENCODING)
            print(timed(text))

        except KeyboardInterrupt:
            sock.close()


if __name__ == '__main__':
    main()
