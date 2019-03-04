# AdminGroup Type asset

from core import bigchaindb
from core.key_pairs import get_appKeyPair
from config import settings

signer = get_appKeyPair()
namespace = '%s.%s' % (settings.APP_NAME, 'admin')

assert signer, 'Application admin key pair must be existed.'


class AdminGroup():
    """ Admin Group Asset Type. We only have one application's admin group type.
    """

    @staticmethod
    def get_or_create():
        """Get or create AdminGroup as an asset.
        """

        metadata = {
            'canLink': [signer.public_key]
        }

        asset = {
            'data': {
                'ns': namespace,
                'name': 'admin'
            }
        }

        return bigchaindb.get_or_create_asset(signer, namespace, asset, metadata)

    @staticmethod
    def get():
        """Get AdminGroup asset already created.
        """
        return bigchaindb.search_asset(signer, namespace)