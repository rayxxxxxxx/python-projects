import argparse

from src.client import Client


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('host', type=str, help='server host')
    argparser.add_argument('port', type=str, help='server port')

    args = argparser.parse_args()

    SERVER_HOST = args.host
    SERVER_PORT = int(args.port)

    client = Client()
    client.connect((SERVER_HOST, SERVER_PORT))

    while True:
        try:
            inmsg = client.recvbytes().decode('utf-8')
            while inmsg:
                print(inmsg)
                inmsg = client.recvbytes().decode('utf-8')

            outmsg = input('> ')
            if outmsg:
                client.sendbytes(outmsg.encode('utf-8'))
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
