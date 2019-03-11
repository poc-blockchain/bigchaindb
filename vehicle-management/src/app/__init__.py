from core import bigchaindb
from core.key_pairs import get_appKeyPair
from core.utils import getLogger
from config import settings

# Create log instance to use across the module
log = getLogger('app')

signer = get_appKeyPair()
namespace = '%s.%s' % (settings.APP_NAME, 'app')

assert signer, 'Application admin key pair must be existed.'


def get_or_create(admin_group_id):
    """Get or create application as an asset.
    """

    metadata = {
        'can_link': [admin_group_id]
    }

    asset = {
        'data': {
            'ns': namespace,
            'name': namespace,
        }
    }

    return bigchaindb.get_or_create_asset(signer, namespace, asset, metadata)


def get():
    """Get application asset already created.
    """
    return bigchaindb.search_asset(signer, asset_ns)
