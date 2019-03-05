# Manage all application asset types:
# DealerGroup, OwnerGroup, PoliceGroup, Incident, and Vehicle

import app
from app.admin import AdminGroup
from asset.dealer import DealerGroup
from asset.vehicle import VehicleGroup
from asset.owner import OwnerGroup
from asset.police import PoliceGroup
from asset.incident import IncidentGroup

from . import log


class AssetTypeManagement():

    @staticmethod
    def generate():
        """
        Generate all asset types in the system.
        """
        # Get or create an AdminGroup Type
        admin_group_id = AdminGroup.get_or_create()

        # Get or create an Application Type managed by admin_group_id
        app_id = app.get_or_create(admin_group_id)

        # Create DealerGroup Asset type
        dealer_group_id = DealerGroup.get_or_create(app_id, admin_group_id)

        # Create OwnerGroup asset type
        owner_group_id = OwnerGroup.get_or_create(app_id, admin_group_id)

        # Create PoliceGroup asset type
        police_group_id = PoliceGroup.get_or_create(app_id, admin_group_id)

        # Create VehicleGroup and only DealerGroup can create vehicle
        vehicle_group_id = VehicleGroup.get_or_create(app_id, dealer_group_id)

        # Create Incident and only PoliceGroup can create Incident
        incident_group_id = IncidentGroup.get_or_create(app_id, police_group_id)

        log.info('The following asset type have been created:')
        log.info('Application id   : %s', app_id)
        log.info('DealerGroup id   : %s', dealer_group_id)
        log.info('OwnerGroup id    : %s', owner_group_id)
        log.info('PoliceGroup id   : %s', police_group_id)
        log.info('VehicleGroup id  : %s', vehicle_group_id)
        log.info('IncidentGroup id : %s', incident_group_id)
