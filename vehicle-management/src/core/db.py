from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import CryptoKeypair

from .operation import Operation


class BigchainDBCore(BigchainDB):

    def __init__(self):
        bdb_root_url = 'https://test.bigchaindb.com'
        super().__init__(bdb_root_url)
        self.namespace = 'vehicle-management'
        self.vehicleapp_ns = self.namespace + '.app'

    def get_or_create_asset(self, signer, asset_ns, asset, metadata):
        """Get or create and asset with asset namespace

            Args:
                signer (AppKeyPair): The key pair to create and commit a transaction.
                asset_ns (str): Namespace for asset.
                asset: (dict): Asset data
                metadata: (dict): Asset metadata
            
            Returns:
                transaction_id (str)
        """
        
        tx_id = self.search_asset(signer, asset_ns)

        # Create if not existed
        if not tx_id:
            tx = self.create_asset(signer, asset, metadata)
            tx_id = tx['id']
        
        return tx_id


    def create_asset(self, signer, asset, metadata):
        """
        Create an asset with namespace
            
            Args:
                signer (AppKeyPair): The key pair to create and commit a transaction.
                asset: (dict): Asset data
            
            Returns:
                transaction_id (str)    
        """
        tx = self.transactions.prepare(
            operation=Operation.CREATE.value,
            signers=signer.public_key,
            asset=asset,
            metadata=metadata,
        )

        signed_tx = self.transactions.fulfill(
            tx,
            private_keys=signer.private_key
        )

        return self.transactions.send_commit(signed_tx)

    def search_asset(self, signer, asset_ns):
        # Get all unspent output for a public address
        outputs = self.outputs.get(signer.public_key, spent=False)

        # Get all assets by namespace across all public keys
        assets = self.assets.get(search=asset_ns)

        # Filter between output and assets to find the application id (transaction id)
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
        return self.transactions.get(asset_id=asset_id)
