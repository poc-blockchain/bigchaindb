from bigchaindb_driver.exceptions import BadRequest


class DuplicateTransaction(BadRequest):
    """Raised if a transaction is duplicated."""
