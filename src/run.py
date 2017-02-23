import sys
import asyncio
from os.path import exists
from weakref import ref

import asyncssh

import config
from config import logger, relative, setup_logging


def key_to_str(key):
    return key.export_public_key().decode()


def get_private_key():
    key_filename = relative(config.PRIVATE_KEY)

    if not exists(key_filename):
        private_key = asyncssh.generate_private_key('ssh-rsa')
        private_key.write_private_key(key_filename)
    else:
        private_key = asyncssh.read_private_key(key_filename)

    return private_key


def collect_info(instance, options=None):
    options = options or config.OPTIONS
    return {
        k: instance.get_extra_info(k)
        for k in options
    }


def log_validation(connection, type, **kwargs):
    data = {
        'type': type,
    }
    data.update(kwargs)
    data['connection'] = collect_info(connection)
    logger.info([
        'validation',
        data,
    ])


class SSHServer(asyncssh.SSHServer):
    def __init__(self):
        super().__init__()
        self._connection = None

    @property
    def connection(self):
        return self._connection()

    def connection_made(self, connection):
        self._connection = ref(connection)

    def begin_auth(self, username):
        return True

    def password_auth_supported(self):
        return True

    def public_key_auth_supported(self):
        return True

    def validate_ca_key(self, username, key):
        log_validation(self.connection,
                       'ca key',
                       username=username,
                       key=key_to_str(key))
        return False

    def validate_public_key(self, username, key):
        log_validation(self.connection,
                       'public key',
                       username=username,
                       key=key_to_str(key))
        return False

    def validate_password(self, username, password):
        log_validation(self.connection,
                       'password',
                       username=username,
                       password=password)
        return False


async def start_server():
    private_key = get_private_key()
    await asyncssh.create_server(SSHServer, config.HOST, config.PORT,
                                 server_version=config.SERVER_VERSION,
                                 server_host_keys=[private_key])
    logger.info(['Started', {
        'host': config.HOST,
        'port': config.PORT,
        'version': config.SERVER_VERSION,
        'server key': key_to_str(private_key),
    }])


def main():
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start_server())
    except (OSError, asyncssh.Error) as exc:
        sys.exit('Error starting server: ' + str(exc))

    loop.run_forever()


if __name__ == '__main__':
    setup_logging()
    main()
