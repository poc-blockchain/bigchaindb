import os

from collections import namedtuple


AppKeyPair = namedtuple('AppKeyPair', ('private_key', 'public_key'))


def get_appKeyPair():
    """
    Read application key pairs from env
    """
    private_key = os.getenv('APP_PRIVATE_KEY')
    public_key = os.getenv('APP_PUBLIC_KEY')

    assert private_key, 'The application private key is empty'
    assert public_key, 'The application public key is empty'

    return AppKeyPair(*(private_key, public_key))
