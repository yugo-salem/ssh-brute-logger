import re
from os import getenv
from os.path import exists, dirname, join, abspath
import logging
import logging.config

import yaml


logger = logging.getLogger('ssh-logger')

relative = lambda *args: abspath(join(dirname(__file__), *args))

HOST = getenv('SSH_HOST', '')
PORT = getenv('SSH_PORT', 8022)
PRIVATE_KEY = getenv('SSH_KEY', 'id_rsa')
SERVER_VERSION = getenv('SERVER_VERSION', 'OpenSSH_7.4')
LOGS_PATH = getenv('LOGS_PATH', relative('.'))

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
        data = yaml.load(input)
        logging.config.dictConfig(data)


class YamlEnvResolver:
    pattern = re.compile(r'^\<%= ENV\[\'(.*)\'\] %\>(.*)$')

    def install(self):
        yaml.add_implicit_resolver('!pathex', self.pattern)
        yaml.add_constructor('!pathex', self.pathex_constructor)

    def pathex_constructor(self, loader, node):
        value = loader.construct_scalar(node)
        variable, remaining = self.pattern.match(value).groups()
        return getenv(variable) + remaining

YamlEnvResolver().install()
