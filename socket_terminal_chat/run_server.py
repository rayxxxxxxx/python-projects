import argparse

from src.server import Server


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('host', type=str, help='server host')
    argparser.add_argument('port', type=str, help='server port')

    args = argparser.parse_args()

    HOST = args.host
    PORT = int(args.port)

    server = Server()
    server.setup((HOST, PORT), 10)
    server.mainloop()


if __name__ == '__main__':
    main()
