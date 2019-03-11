from core import bigchaindb
from core.key_pairs import get_appKeyPair
from core.utils import current_time

import app

from . import log

signer = get_appKeyPair()


class AssetType():
    """ Abstract AssetType class
    """

    # Each Id present for an unique AssetType.
    id = None

    @staticmethod
    def get_name():
        """
        Asset type name. Child class implement this function
        """
        raise NotImplementedError("Need implementation.")

    @classmethod
    def get_asset_ns(cls):
        """
        Asset namespace.
        """
        return '%s.%s' % (app.namespace, cls.get_name())

    @classmethod
    def get_instance_ns(cls, public_key):
        """
        Return the namespace of asset type instance.
        """
        return '%s.%s' % (cls.get_asset_ns(), public_key)

    @classmethod
    def get_or_create(cls, app_id, can_link):
        """
        Get or create an specific asset type.
        """
        namespace = cls.get_asset_ns()
        metadata = {
            'can_link': can_link
        }

        asset = {
            'data': {
                'ns': namespace,
                'link': app_id,
                'name': cls.get_name()
            }
        }

        # Retrieve or create new asset type
        cls.id = bigchaindb.get_or_create_asset(
            signer, namespace, asset, metadata)

        return cls.id

    @classmethod
    def get(cls, asset_id=None):
        """
        Get asset type group id
        """
        if asset_id is None:
            asset_ns = cls.get_asset_ns()
            asset_id = bigchaindb.search_asset(signer, asset_ns)

        return bigchaindb.get(asset_id)

    @classmethod
    def create_instance(cls, public_key):
        """
        Assign to DealerGroup
        """

        # The AssetType id must be created or retrieved
        # before creating a new instance
        assert cls.id, 'The {class_name} id must be set. Please run {class_name}.get_or_create()'.format(cls.__name__) # noqa

        tx_id = cls.get_granted_permission(public_key)

        if tx_id is not None:
            log.info(
                'The key %s is already exsited in this transaction id %s',
                public_key,
                tx_id)
            return tx_id

        metadata = {
            'event': 'Created %s instance' % (cls.__name__),
            'created_at': current_time(),
            'eventData': {
                'assetType': cls.get_name()
            },
            'publicKey': signer.public_key
        }

        asset = {
            'data': {
                'link': cls.id,
                'ns': cls.get_instance_ns(public_key)
            }
        }

        recipients = (public_key)
        tx_id = bigchaindb.create_asset(
            signer, asset, metadata, recipients=recipients)
        log.info(
            'The key %s is linked to %s in this transaction id %s',
            public_key,
            cls.__name__,
            tx_id)

    @classmethod
    def get_granted_permission(cls, public_key):
        """
        Check wether a public key is granted admin right.

        Args:
            public_key (str): The public key to check permison is granted

        Returns:
            Transaction Id (str) if admin right is granted otherwise None
        """
        namespace = cls.get_instance_ns(public_key)
        return bigchaindb.search_asset(public_key, namespace)
