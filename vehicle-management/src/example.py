from datetime import datetime
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
conn = BigchainDB('https://test.bigchaindb.com')
namespace = 'ibpb.tranhoang'

def createNewAsset(keypair, asset, metadata):
    tx = conn.transactions.prepare(
        operation='CREATE',
        signers=keypair.public_key,
        asset=asset,
        metadata=metadata,
        recipients=(keypair.public_key),
    )

    signed_tx = conn.transactions.fulfill(
        tx,
        private_keys=keypair.private_key
    )
    return conn.transactions.send_commit(signed_tx)

def transferAsset(tx, fromKeyPair, toPublicKey, metadata):

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
   
    prepared_transfer_tx = conn.transactions.prepare(
        operation='TRANSFER',
        asset=transfer_asset,
        inputs=transfer_input,
        recipients=toPublicKey,
    )

    fulfilled_transfer_tx = conn.transactions.fulfill(
        prepared_transfer_tx,
        private_keys=fromKeyPair.private_key,
    )
    sent_transfer_tx = conn.transactions.send_commit(fulfilled_transfer_tx)
    
    return sent_transfer_tx

# 
# admin1, adminGroupId, 'admin', admin1.publicKey, adminuser1Metadata)
def createUser(adminKeyPair, userTypeId, userTypeName, userPublicKey, userMetadata):
    asset = {
        'data': {
            'ns': '%s.%s' % (namespace, userTypeName),
            'link': userTypeId,
            'createdBy': adminKeyPair.public_key,
            'type': userTypeName,
            'keyword': 'UserAsset'
        }
    }

    metadata = {
        'event': 'User Added',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'timestamp': datetime.now().timestamp(),
        'publicKey': adminKeyPair.public_key,
        'eventData': {
            'userType': userTypeName
        }
    }
    instanceTx = createNewAsset(adminKeyPair, asset, metadata)
    transferAsset(instanceTx, adminKeyPair, userPublicKey, userMetadata)
    return instanceTx

def createType(typeName, appId, canLinkAssetId):
    asset = {
        'data': {
            'ns': '%s.%s' % (namespace, typeName),
            'link': appId,
            'name': typeName
        }
    }

    metadata = {
        'can_link': canLinkAssetId
    }

    return createNewAsset(admin1, asset, metadata)


def createTypeInstance(keypair, typeName, typeId, metadata):
    asset = {
        'data': {
            'ns': '%s.%s' % (namespace, typeName),
            'link': typeId
        }
    }

    return createNewAsset(keypair, asset, metadata)


# Create admin type
admin1 = generate_keypair()

adminGroupAsset = {
    'data': {
        'ns': '%s.%s' % (namespace, 'admin'),
        'name': 'admin'
    }
}

adminGroupMetadata = {
    'canLink': [admin1.public_key]
}

tx = createNewAsset(admin1, adminGroupAsset, adminGroupMetadata)
adminGroupId = tx['id']

# Create app
appAsset = {
    'data': {
        'ns': namespace,
        'name': namespace
    }
}
appMetadata = {
    'canLink': adminGroupId
}

app = createNewAsset(admin1, appAsset, appMetadata)
appId = app['id']


user1 = generate_keypair()
user2 = generate_keypair()
user3 = generate_keypair()

adminuser1Metadata = {
    'event': 'User Assigned',
    'date': datetime.now().strftime('%Y-%m-%d'),
    'timestamp': datetime.now().timestamp(),
    'publicKey': admin1.public_key,
    'eventData': {
        'userType': 'admin'
    }
}

adminUserId = createUser(admin1, adminGroupId, 'admin', admin1.public_key, adminuser1Metadata).id


# Tribes are user groups
tribe1Id = createType('tribe1', appId, adminGroupId)['id']
tribe2Id = createType('tribe2', appId, adminGroupId)['id']


# Add user1 to tribe1 group
user1Metadata = {
    'event': 'User Assigned',
    'date': datetime.now().strftime('%Y-%m-%d'),
    'timestamp': datetime.now().timestamp(),
    'publicKey': admin1.public_key,
    'eventData': {
        'userType': 'tribe1'
    }
}
user1AssetId = createUser(admin1, tribe1Id, 'tribe1', user1.public_key, user1Metadata)['id']

# Add user2 to tribe2 group
user2Metadata = {
    'event': 'User Assigned',
    'date': datetime.now().strftime('%Y-%m-%d'),
    'timestamp': datetime.now().timestamp(),
    'publicKey': admin1.public_key,
    'eventData': {
        'userType': 'tribe2'
    }
}
user2AssetId = createUser(admin1, tribe2Id, 'tribe2', user2.public_key, user2Metadata)['id']


# Add user3 to tribe1 group
user3Metadata = {
    'event': 'User Assigned',
    'date': datetime.now().strftime('%Y-%m-%d'),
    'timestamp': datetime.now().timestamp(),
    'publicKey': admin1.public_key,
    'eventData': {
        'userType': 'tribe1'
    }
}
user3AssetId = createUser(admin1, tribe1Id, 'tribe1', user3.public_key, user3Metadata)['id']

# Only tribe 1 users can create proposal
proposalGroupId = createType('proposal', appId, tribe1Id)['id']

# Only tribe 2 users can create vote
voteGroupId = createType('vote', appId, tribe2Id)['id']


# create proposal by user 1 - should pass
proposal1 = createTypeInstance(
    user1,
    'proposal',
    proposalGroupId,
    { 'name': 'new proposal by user 1', 'timestamp': datetime.now().timestamp() })

# create vote by user 2 - should pass
vote1 = createTypeInstance(
    user2,
    'vote',
    voteGroupId,
    { 'name': 'new vote by user 2', 'timestamp': datetime.now().timestamp() })

# create proposal by user 3 - should pass
proposal2 = createTypeInstance(
    user3,
    'proposal',
    proposalGroupId,
    { 'name': 'new proposal by user 3', 'timestamp': datetime.now().timestamp() })

# create vote by user 1 - should fail
vote2 = createTypeInstance(
    user1,
    'vote',
    voteGroupId,
    { 'name': 'new vote by user 1', 'timestamp': datetime.now().timestamp() })