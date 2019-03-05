# DealerGroup type asset

from .types import AssetType

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
