from pathlib import Path
import socket
import configparser

import src.utils.networking as sockutil
from modules.data_token import DataToken

conf = configparser.ConfigParser()
conf.read(Path('config.conf'))

ENCODING = conf.get('SYSTEM', 'ENCODING')
HEADER_SIZE = int(conf.get('SYSTEM', 'HEADER_SIZE'))
BUFFER_SIZE = int(conf.get('SYSTEM', 'BUFFER_SIZE'))


class ChatClient:
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, addr: tuple) -> None:
        try:
            self.sock.connect(addr)
            self.sock.setblocking(False)
        except ConnectionRefusedError:
            self.sock.close()
            exit(1)

    def disconnect(self) -> None:
        sockutil.sendbytes(self.sock, DataToken.DISCONNECT.value)
        self.sock.close()

    def mainloop(self):
        while True:
            try:
                try:
                    data = sockutil.recvstr(self.sock)
                    while data:
                        print(data)
                        data = sockutil.recvstr(self.sock)
                except BlockingIOError:
                    pass

                msg = input('> ')
                if msg:
                    sockutil.sendstr(self.sock, msg)
            except KeyboardInterrupt:
                self.disconnect()
                break


def main():
    SERVER_HOST = conf.get('SERVER', 'HOST')
    SERVER_PORT = int(conf.get('SERVER', 'PORT'))

    client = ChatClient()
    client.connect((SERVER_HOST, SERVER_PORT))
    client.mainloop()


if __name__ == '__main__':
    main()
