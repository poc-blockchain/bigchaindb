# IncidentGroup type asset

from .types import AssetType


class IncidentGroup(AssetType):
    """ PoliceGroup type asset in application.
    All incidents instance are linked to this type.
    """

    @staticmethod
    def get_name():
        """
        Asset type name
        """
        return 'incident'
