# Manage all application asset types:
# DealerGroup, OwnerGroup, PoliceGroup, Incident, and Vehicle

import app
from app.admin import AdminGroup
from asset.dealer import DealerGroup, Dealer
from asset.vehicle import VehicleGroup
from asset.owner import OwnerGroup
from asset.police import PoliceGroup, Police
from asset.incident import IncidentGroup

from . import log


class AssetTypeManagement():

    @classmethod
    def generate(cls):
        """
        Generate all asset types in the system.
        """

        # Get or create an AdminGroup Type
        cls.admin_group_id = AdminGroup.get_or_create()

        # Get or create an Application Type managed by admin_group_id
        cls.app_id = app.get_or_create(cls.admin_group_id)

        # Create an admin
        AdminGroup.assign()

        # Create DealerGroup Asset type
        cls.dealer_group_id = DealerGroup.get_or_create(
            cls.app_id, cls.admin_group_id)

        # Create OwnerGroup asset type
        cls.owner_group_id = OwnerGroup.get_or_create(
            cls.app_id, cls.admin_group_id)

        # Create PoliceGroup asset type
        cls.police_group_id = PoliceGroup.get_or_create(
            cls.app_id, cls.admin_group_id)

        # Create VehicleGroup and only DealerGroup can create vehicle
        cls.vehicle_group_id = VehicleGroup.get_or_create(
            cls.app_id, cls.dealer_group_id)

        # Create Incident and only PoliceGroup can create Incident
        cls.incident_group_id = IncidentGroup.get_or_create(
            cls.app_id, cls.police_group_id)

        log.info('The following asset type have been created:')
        log.info('Application id   : %s', cls.app_id)
        log.info('DealerGroup id   : %s', cls.dealer_group_id)
        log.info('OwnerGroup id    : %s', cls.owner_group_id)
        log.info('PoliceGroup id   : %s', cls.police_group_id)
        log.info('VehicleGroup id  : %s', cls.vehicle_group_id)
        log.info('IncidentGroup id : %s', cls.incident_group_id)

    def test(self):
        """
        Test create asset
        """
        log.info('Create a dealer')
        dealer = self.create_dealer()
        log.info('Create a police')
        police = self.create_police()

        # A dealer can create an vehicle
        vehicle_id = dealer.create_asset(
            AssetTypeManagement.vehicle_group_id, 'vehicle', 'Vehicle #1')

        # A police can create an incident of a vehicle
        police.create_asset(
            AssetTypeManagement.incident_group_id,
            'incident',
            vehicle_id,
            'A scratch on car bumper')

        # A dealer can't create an incident - should fail
        try:
            dealer.create_asset(
                AssetTypeManagement.incident_group_id,
                'incident',
                'Incident #1')
        except Exception as err:
            log.error('A dealer cant create incident. Error in details:')
            log.error(err)

        # A police can't create an vehicle - should fail
        try:
            police.create_asset(
                AssetTypeManagement.vehicle_group_id,
                'vehicle',
                'Vehicle #1',
                '')
        except Exception as err:
            log.error('A police cant create an vehicle. Error in details:')
            log.error(err)

    def create_dealer(self, public_key=None):
        """
        Generate an key/pair and link public key to dealer group
        """
        # In this example we will read one dealer key pairs from the .env file.
        # In real application the dealers have to generate their own key pairs
        # and provide the public key to the application
        # to grant the dealer privileged.
        dealer = Dealer(public_key=public_key)
        dealer.save(app.signer)
        return dealer

    def create_police(self, public_key=None):
        """
        Generate an key/pair and link public key to police group
        """
        # In this example we will read one police key pairs from the .env file.
        # In real application the polices have to generate their own key pairs
        # and provide the public key to the application
        # to grant the police privileged.
        police = Police(public_key=public_key)
        police.save(app.signer)
        return police
