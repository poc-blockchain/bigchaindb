# AdminGroup Type asset
from core import bigchaindb
from core.key_pairs import get_appKeyPair
from config import settings

from . import log

signer = get_appKeyPair()
namespace = '%s.%s' % (settings.APP_NAME, 'admin')

assert signer, 'Application admin key pair must be existed.'


class AdminGroup():
    """ Admin Group Asset Type. We only have one application's admin group type.
    """

    # We only have one application's admin group type.
    id = None

    @staticmethod
    def get_or_create():
        """Get or create AdminGroup as an asset.
        """

        metadata = {
            'can_link': [signer.public_key]
        }

        asset = {
            'data': {
                'ns': namespace,
                'name': 'admin'
            }
        }

        # There is only one AdminGroup in the application
        # Assign the only admin group id to AdminGroup class
        AdminGroup.id = bigchaindb.get_or_create_asset(
            signer, namespace, asset, metadata)

        return AdminGroup.id

    @staticmethod
    def get():
        """Get AdminGroup asset already created.
        """
        return bigchaindb.search_asset(signer, namespace)

    @staticmethod
    def get_instance_ns(admin_public_key):
        """
        Return the namespace of admin user.
        """
        return '%s.%s' % (namespace, admin_public_key)

    @classmethod
    def assign(cls):
        """
        Create admin user
        """

        # The AdminGroup type id must be created before assign any admin user
        assert cls.id, \
            'The AdminGroup Type id must be set. Please run AdminGroup.get_or_create()' # noqa

        metadata = {
            'event': 'User Assigned',
            'publicKey': signer.public_key,
            'eventData': {
                'userType': 'admin'
            }
        }

        tx_id = bigchaindb.createUser(
            signer,
            cls.id,
            'admin',
            signer.public_key,
            metadata,
            can_link=signer.public_key)

        log.info(
            'Admin user has been create in transaction %s',
            tx_id)

        return tx_id

    @classmethod
    def get_granted_permission(cls, admin_public_key):
        """
        Check wether a public key is granted admin right.

        Args:
            admin_public_key (str): The public key to check permison is granted

        Returns:
            Transaction Id (str) if admin right is granted otherwise None
        """
        namespace = cls.get_instance_ns(admin_public_key)
        return bigchaindb.search_asset(admin_public_key, namespace)
