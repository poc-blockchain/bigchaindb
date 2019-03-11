# VehicleGroup asset type

from .types import AssetType


class VehicleGroup(AssetType):
    """ VehicleGroup type asset in application.
    All vehicles instance are linked to this type.
    """

    @staticmethod
    def get_name():
        """
        Asset type name
        """
        return 'vehicle'

