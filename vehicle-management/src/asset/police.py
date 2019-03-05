# PoliceGroup type asset

from .types import AssetType

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
