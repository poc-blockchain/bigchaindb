import re

from bigchaindb_driver import BigchainDB
from bigchaindb_driver.exceptions import BadRequest

from .exceptions import DuplicateTransaction
from .operation import Operation


class BigchainDBCore(BigchainDB):

    def __init__(self):
        bdb_root_url = 'http://localhost:9984'
        super().__init__(bdb_root_url)
        self.namespace = 'vehicle-management'
        self.vehicleapp_ns = self.namespace + '.app'

    def get_or_create_asset(self, signer, asset_ns, asset, metadata):
        """Get or create and asset with asset namespace

            Args:
                signer (AppKeyPair): The key pair to create and commit a transaction. # noqa
                asset_ns (str): Namespace for asset.
                asset: (dict): Asset data
                metadata: (dict): Asset metadata

            Returns:
                transaction_id (str)
        """
        try:
            return self.create_asset(signer, asset, metadata)
        except DuplicateTransaction as err:
            return err.args[0]

    def create_asset(self, signer, asset, metadata, recipients=None):
        """
        Create an asset with namespace

            Args:
                signer (AppKeyPair): The key pair to create and commit a transaction. # noqa
                asset: (dict): Asset data

            Returns:
                transaction_id (str)    
        """
        try:
            tx = self.transactions.prepare(
                operation=Operation.CREATE.value,
                signers=signer.public_key,
                asset=asset,
                metadata=metadata,
                recipients=recipients,
            )

            signed_tx = self.transactions.fulfill(
                tx,
                private_keys=signer.private_key
            )

            tx = self.transactions.send_commit(signed_tx)
            return tx['id']
        except BadRequest as err:
            tx_id = self.find_tx_id(err)
            if tx_id is not None:
                raise DuplicateTransaction(tx_id)
            else:
                raise err
        except Exception as err:
            raise err

    def transferAsset(self, tx, fromKeyPair, toPublicKey, metadata):
        """
        Transfer asset (tx) fromKeyPair to toPublicKey
        """

        asset_id = tx['id']
        transfer_asset = {
            'id': asset_id,
        }

        output_index = 0
        output = tx['outputs'][output_index]

        transfer_input = {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output_index': output_index,
                'transaction_id': tx['id'],
            },
            'owners_before': output['public_keys'],
        }

        prepared_transfer_tx = self.transactions.prepare(
            operation=Operation.TRANSFER.value,
            asset=transfer_asset,
            inputs=transfer_input,
            recipients=toPublicKey,
        )

        fulfilled_transfer_tx = self.transactions.fulfill(
            prepared_transfer_tx,
            private_keys=fromKeyPair.private_key,
        )
        sent_transfer_tx = self.transactions.send_commit(fulfilled_transfer_tx)

        return sent_transfer_tx

    def search_asset(self, public_key, asset_ns):
        # Get all unspent output for a public address
        outputs = self.outputs.get(public_key, spent=False)

        # Get all assets by namespace across all public keys
        assets = self.assets.get(search=asset_ns)

        # Filter between output and assets to find the application id (transaction id) # noqa
        transaction_id = None
        unspent_txs = [output['transaction_id'] for output in outputs]
        for asset in assets:
            if asset['data'].get('ns', '') == asset_ns \
                    and asset['id'] in unspent_txs:
                transaction_id = asset['id']
                break

        return transaction_id

    def get(self, asset_id=None):
        """
        Get asset by id
        """
        txs = self.transactions.get(asset_id=asset_id)
        if txs is not None and len(txs) > 1:
            raise Exception(
                'There is more than one transaction with id %s' % asset_id)

        return txs[0]

    def createUser(
            self,
            key_pair,
            user_type_id,
            user_type_name,
            user_public_key,
            user_metadata,
            can_link=None):
        asset = {
            'data': {
                'ns': '%s.%s' % (self.namespace, user_type_name),
                'link': user_type_id,
                'createdBy': key_pair.public_key,
                'type': user_type_name,
                'keyword': 'UserAsset'
            }
        }

        metadata = {
            'event': 'User Added',
            'publicKey': key_pair.public_key,
            'eventData': {
                'userType': user_type_name
            }
        }

        if can_link is not None:
            metadata['can_link'] = can_link

        try:
            instanceTx_id = self.create_asset(key_pair, asset, metadata)
            instanceTx = self.get(asset_id=instanceTx_id)
            self.transferAsset(
                instanceTx, key_pair, user_public_key, user_metadata)
        except DuplicateTransaction as err:
            instanceTx_id = err.args[0]

        return instanceTx_id

    def find_tx_id(self, err):
        """
        Find transaction id from exception message
        """
        tx_id = None
        if len(err.args) >= 3 \
                and 'DuplicateTransaction' in err.args[2]['message']:
            message = err.args[2]['message']
            pattern = r'.*?`(.*)`.*'
            tx_id = re.search(pattern, message).group(1)
        return tx_id
