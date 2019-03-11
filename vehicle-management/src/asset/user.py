from core import bigchaindb

from . import log


class User():
    """
    Police instance asset
    """
    def __init__(self, group_id, group_name, user_public_key):
        self.group_id = group_id
        self.group_name = group_name
        self.user_public_key = user_public_key

    def save(self, signer):
        """
        Create police instance as an asset
        """
        metadata = {
            'event': 'User Assigned',
            'publicKey': signer.public_key,
            'eventData': {
                'userType': self.group_name
            }
        }

        tx_id = bigchaindb.createUser(
            signer,
            self.group_id,
            self.group_name,
            self.user_public_key,
            metadata,
            can_link=signer.public_key)

        log.info(
            '%s user has been create in transaction %s',
            self.group_name,
            tx_id)

        return tx_id
