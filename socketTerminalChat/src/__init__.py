from pathlib import Path
import configparser

conf = configparser.ConfigParser()
conf.read(Path('config.ini'))

ENCODING = conf.get('SYSTEM', 'ENCODING')
HEADER_SIZE = int(conf.get('SYSTEM', 'HEADER_SIZE'))
BUFFER_SIZE = int(conf.get('SYSTEM', 'BUFFER_SIZE'))
