# IncidentGroup type asset

from .types import AssetType


class OwnerGroup(AssetType):
    """ OwnerGroup type asset in application.
    All owners instance are linked to this type.
    """

    @staticmethod
    def get_name():
        """
        Asset type name
        """
        return 'owner'
