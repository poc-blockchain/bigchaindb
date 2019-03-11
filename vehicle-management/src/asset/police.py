# PoliceGroup type asset
from core import bigchaindb
from core.utils import current_time
from core.key_pairs import load_test_key_pair
from .types import AssetType
from .user import User


class PoliceGroup(AssetType):
    """ PoliceGroup type asset in application.
    All polices instance are linked to this type.
    """

    @staticmethod
    def get_name():
        """
        Asset type name
        """
        return 'police'


class Police(User):
    """
    Police instance asset
    """

    def __init__(self, public_key=None):

        if public_key is None:
            self.load_test_key_pair()

        super().__init__(
            PoliceGroup.id, PoliceGroup.get_name(), self.key_pairs.public_key)

    def load_test_key_pair(self):
        """
        Load test key pair
        """
        self.key_pairs = load_test_key_pair(
            'POLICE_PRIVATE_KEY', 'POLICE_PUBLIC_KEY')

    def create_asset(
            self,
            asset_type_id,
            asset_type_name,
            vehicle_id,
            incident_data):
        """
        Create an asset
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
                'vehicle_id': vehicle_id,
                'incident': incident_data
            }
        }

        tx_id = bigchaindb.create_asset(self.key_pairs, asset, metadata)
        return tx_id
