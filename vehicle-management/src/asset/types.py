from core import bigchaindb
from core.key_pairs import get_appKeyPair

import app

signer = get_appKeyPair()


class Type():
    """ Abstract type class
    """

    def __init__(self):
        pass
    
    def get_name(self):
        """
        Asset type name. Child class implement this function
        """
        raise NotImplementedError("Need implementation.")

    def get_asset_ns(self):
        """
        Asset namespace.
        """
        asset_ns = '%s.%s' % (app.app_ns, self.get_name())


class Admin():
    """
    Admin type asset in application.
    All users has admin rights is linked to this Type.
    """
    pass


class Dealer():
    """
    Dealer type asset in application.
    All dealers instance are linked to this Type.
    """
    pass


class Owner():
    """
    Asset owner type in application.
    All owners instance are linked to this Type.
    """


class Vehicle():
    """
    Vehicle type in application.
    All vehicles instance are linked to this Type.
    """
    pass


class Incident():
    """
    Incident type in application.
    All incidents are linked to this Type.
    """
    pass