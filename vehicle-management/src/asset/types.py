from core import bigchaindb
from core.key_pairs import get_appKeyPair

import app

signer = get_appKeyPair()


class AssetType():
    """ Abstract AssetType class
    """

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
    def get_or_create(cls, app_id, can_link):
        """
        Get or create an specific asset type.
        """
        namespace = cls.get_asset_ns()
        metadata = {
            'link': app_id,
            'canLink': [can_link]
        }

        asset = {
            'data': {
                'ns': namespace,
                'name': cls.get_name()
            }
        }

        # Retrieve or create new asset type
        cls.id = bigchaindb.get_or_create_asset(signer, namespace, asset, metadata)

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
    def load_asset_type_id(cls):
        """
        Load asset type id and store in cls.id
        """
        