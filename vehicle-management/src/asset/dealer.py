# DealerGroup type asset
from core import bigchaindb
from core.key_pairs import load_test_key_pair
from core.utils import current_time
from .types import AssetType
from .user import User


class DealerGroup(AssetType):
    """ Dealer type asset in application.
    All dealers instance are linked to this Type.
    """

    @staticmethod
    def get_name():
        """
        Asset type name
        """
        return 'dealer'


class Dealer(User):

    def __init__(self, public_key=None):
        if public_key is None:
            self.load_test_key_pair()

        super().__init__(
            DealerGroup.id, DealerGroup.get_name(), self.key_pairs.public_key)

    def load_test_key_pair(self):
        """
        Load test key pair
        """
        self.key_pairs = load_test_key_pair(
            'DEALER_PRIVATE_KEY', 'DEALER_PUBLIC_KEY')

    def create_asset(self, asset_type_id, asset_type_name, vehicle_id):
        """
        Create an vehicle
        """
        metadata = {
            'event': 'Created asset %s' % asset_type_name,
            'created': current_time(),
            'eventData': {
                'assetType': asset_type_name
            },
        }

        asset = {
            'data': {
                'link': asset_type_id,
                'ns': 'vehicle-mangement.app.%s' % asset_type_name,
                'id': vehicle_id
            }
        }

        tx_id = bigchaindb.create_asset(self.key_pairs, asset, metadata)
        return tx_id
