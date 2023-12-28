from pathlib import Path
import configparser

from src.client import Client


def main():
    conf = configparser.ConfigParser()
    conf.read(Path('config.ini'))

    SERVER_HOST = conf.get('SERVER', 'HOST')
    SERVER_PORT = int(conf.get('SERVER', 'PORT'))

    client = Client()
    client.connect((SERVER_HOST, SERVER_PORT))

    client.sendbytes(b"\r\0")


if __name__ == '__main__':
    main()
