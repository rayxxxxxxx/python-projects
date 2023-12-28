from pathlib import Path
import configparser

conf = configparser.ConfigParser()
conf.read(Path('config.conf'))

HOST = conf.get('SERVER', 'HOST')
PORT = int(conf.get('SERVER', 'PORT'))

ENCODING = conf.get('SYSTEM', 'ENCODING')
HEADER_SIZE = int(conf.get('SYSTEM', 'HEADER_SIZE'))
BUFFER_SIZE = int(conf.get('SYSTEM', 'BUFFER_SIZE'))
