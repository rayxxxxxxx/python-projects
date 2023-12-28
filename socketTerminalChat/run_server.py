from pathlib import Path
import configparser

from src.server import Server


def main():
    conf = configparser.ConfigParser()
    conf.read(Path('config.conf'))

    HOST = conf.get('SERVER', 'HOST')
    PORT = int(conf.get('SERVER', 'PORT'))

    server = Server()
    server.setup((HOST, PORT), 10)
    server.mainloop()


if __name__ == '__main__':
    main()
