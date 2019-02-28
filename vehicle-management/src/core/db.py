from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import CryptoKeypair

from .operation import Operation


class BigchainDBCore(BigchainDB):

    def __init__(self):
        bdb_root_url = 'https://test.bigchaindb.com'
        super().__init__(bdb_root_url)

    def create_app(self, namespace, signer):
        """Create application as an asset
        
            Args:
                namespace (str) added to asset.data which we use to
                    make it easy to search assets of a particular type in BigchainDB.
                signer (CryptoKeypair): The key pair to create and commit a transaction.
        """
        assert namespace, 'namespace is required.'

        tx = self.transactions.prepare(
            operation=Operation.CREATE,
            signers=signer.public_key,
            asset={
                'ns': namespace,
                'name': 'Vehicle management application',
                'data': {
                    'message': 'A vehicle management RBAC application.'
                }
            }
        )

        signed_tx = self.transactions.fulfill(
            tx,
            private_keys=signer.private_key
        )

        return self.transactions.send_commit(signed_tx)
