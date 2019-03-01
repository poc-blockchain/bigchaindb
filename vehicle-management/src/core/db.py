from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import CryptoKeypair

from .operation import Operation


class BigchainDBCore(BigchainDB):

    def __init__(self):
        bdb_root_url = 'https://test.bigchaindb.com'
        super().__init__(bdb_root_url)
        self.namespace = 'vehicle-management'
        self.vehicleapp_ns = self.namespace + '.app'

    def create_app(self, signer):
        """Create application as an asset
        
            Args:
                namespace (str) added to asset.data which we use to
                    make it easy to search assets of a particular type in BigchainDB.
                signer (CryptoKeypair): The key pair to create and commit a transaction.
        """

        tx = self.transactions.prepare(
            operation=Operation.CREATE.value,
            signers=signer.public_key,
            asset={
                'data': {
                    'ns': self.vehicleapp_ns,
                    'name': 'Vehicle management application',
                    'message': 'A vehicle management RBAC application.'
                }
            }
        )

        signed_tx = self.transactions.fulfill(
            tx,
            private_keys=signer.private_key
        )

        return self.transactions.send_commit(signed_tx)

    def search_app(self, signer):

        # Get all unspent output for a public address
        outputs = self.outputs.get(signer.public_key, spent=False)

        # Get all assets by namespace across all public keys
        assets = self.assets.get(search=self.vehicleapp_ns)

        # Filter between output and assets to find the application id (transaction id)
        transaction_id = None
        unspent_txs = [output['transaction_id'] for output in outputs]
        for asset in assets:
            if asset['data'].get('ns', '') == self.vehicleapp_ns \
                and asset['id'] in unspent_txs:
                    transaction_id = asset['id']
                    break

        return transaction_id
