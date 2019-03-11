import os
from collections import namedtuple

AppKeyPair = namedtuple('AppKeyPair', ('private_key', 'public_key'))


def get_appKeyPair():
    """
    Read application key pairs from env
    """
    return load_test_key_pair('APP_PRIVATE_KEY', 'APP_PUBLIC_KEY')


def load_test_key_pair(private_key_name, public_key_name):
    """
    Load key pair for testing
    """
    private_key = os.getenv(private_key_name)
    public_key = os.getenv(public_key_name)

    assert private_key, 'The private key is empty'
    assert public_key, 'The public key is empty'

    return AppKeyPair(*(private_key, public_key))    