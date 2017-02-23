from os import getenv
from os.path import exists, dirname, join
import logging
import logging.config

import yaml


logger = logging.getLogger('ssh-logger')

relative = lambda *args: join(dirname(__file__), *args)

HOST = getenv('SSH_HOST', '')
PORT = getenv('SSH_PORT', 8022)
PRIVATE_KEY = getenv('SSH_KEY', 'id_rsa')
SERVER_VERSION = getenv('SERVER_VERSION', 'OpenSSH_7.4')

OPTIONS = [
    'sockname',
    'peername',
    'username',
    'client_version',
    'recv_cipher',
    'recv_compression',
    'recv_mac',
    'send_cipher',
    'send_compression',
    'send_mac',
    'server_version',
]


def setup_logging():
    config_filename = relative('logging.yaml')

    if not exists(config_filename):
        logging.basicConfig(level=logging.DEBUG)
        return

    with open(config_filename, 'r') as input:
        data = yaml.safe_load(input)
        logging.config.dictConfig(data)
