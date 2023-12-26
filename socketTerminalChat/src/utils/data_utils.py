from pathlib import Path
import configparser

conf = configparser.ConfigParser()
conf.read(Path('config.conf'))

HEADER_SIZE = int(conf.get('SYSTEM', 'HEADER_SIZE'))


def add_header(data: bytes):
    dsize = len(data)
    ndigits = len(str(dsize))
    header = str(dsize).encode()+b' '*(HEADER_SIZE-ndigits)
    return header+data
