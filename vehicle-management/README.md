# Vehicle Management

## Environment Prerequisite

1. Docker
2. Git
3. Python >= 3.5

## Start the bigchaindb with RBAC feature on local

``` bash
git clone git@github.com:bigchaindb/bigchaindb.git
cd bigchaindb
git checkout rbac
make run
```

## Set up local development

``` bash
git clone git@github.com:poc-blockchain/bigchaindb.git
```

### Install pipenv

``` bash
brew install pipenv
```

### Setup virtual env

``` bash
cd vehicle-management
pipenv --python 3.5
pipenv shell
```

### Instal dependencies

``` bash
cd vehicle-management
pipenv install
```

### Set up env variables

1. We can use the following scripts to generate the keypairs

``` python
from bigchaindb_driver.crypto import generate_keypair
generate_keypair()
```

Then copy the key pairs to .env file in next step.

2. Create an .env file under the vehicle-management/src folder
with the following keys.

``` env
APP_NAME='vehicle-mangement'
APP_PUBLIC_KEY='Application public key'
APP_PRIVATE_KEY='Application private key'

# Dealer key pairs. In real application the dealer has to generate their own key pairs
# and provide the public key to the application to grant the dealer privileged
DEALER_PUBLIC_KEY='Dealer public key'
DEALER_PRIVATE_KEY='Dealer private key'

# Police key pairs. In real application the police has to generate their own key pairs
# and provide the public key to the application to grant the police privileged
POLICE_PUBLIC_KEY='Police public key'
POLICE_PRIVATE_KEY='Police private key'
```

### Error when commit a transaction on MacOS

``` text
ssl.SSLError: [SSL: TLSV1_ALERT_PROTOCOL_VERSION] tlsv1
```

On MacOS run pip install pip install 'requests[security]' to fix that issue.

### Run code example

#### 1. Setup application type and asset types

``` python
from asset.management import AssetTypeManagement
AssetTypeManagement.generate()
```

Output

``` console
asset - INFO - The following asset type have been created:
asset - INFO - Application id   : 565220379e71cca4d549b3a8a8f34a96f37d20894e4a95fb7e5c4ea4e65db3b4
asset - INFO - DealerGroup id   : 87df8da6ec807a68397a63b627c3f6b8651c1e63178497bbc64a76219e9aceb1
asset - INFO - OwnerGroup id    : ff5478866af1c4ad369c3a104730dc544939f7da4d49f39276d7b442c39d7e32
asset - INFO - PoliceGroup id   : 2adef58aeedea999a4809c118f148c5e2a841c731ce8c68f5e23e5980bdfbead
asset - INFO - VehicleGroup id  : 9512a9d17a68c8154326b3b89b36b8a853dc03a911ee7a8eb23a1f623a8e3043
asset - INFO - IncidentGroup id : c66be9523ab5e3daefa8b032aab58bb2380fb0fb84c27a7d7f53750b9753b9da
```

#### 2. Test create asset by role

``` python
from asset.management import AssetTypeManagement
AssetTypeManagement.generate()
manager = AssetTypeManagement()
manager.test()
```

Output

``` console
asset - INFO - Create a dealer
asset - INFO - dealer user has been create in transaction 17f5af89189d2581a676df84ec228bc1cac1fb92f091f3086638329b6abea5f5
asset - INFO - Create a police
asset - INFO - police user has been create in transaction 9490982c2558c0cba00359e77419db5aeb141f2461b22928bb1a682e6bd5ab8f
asset - ERROR - A dealer cant create incident
asset - ERROR - (400, '{"message":"Invalid transaction (ValidationError): Linking is not authorized for: YdiL1LU4bsxnenQf9rJUdH8HGin6nh9aRPdjPEmkJNP","status":400}\n', {'message': 'Invalid transaction (ValidationError): Linking is not authorized for: YdiL1LU4bsxnenQf9rJUdH8HGin6nh9aRPdjPEmkJNP', 'status': 400}, 'http://localhost:9984/api/v1/transactions/')
asset - ERROR - A police cant create an vehicle
asset - ERROR - (400, '{"message":"Invalid transaction (ValidationError): Linking is not authorized for: bCUQr7bjq3WKBDEkymdCYS7ck5XVsBzBGhnEQdhh7HJ","status":400}\n', {'message': 'Invalid transaction (ValidationError): Linking is not authorized for: bCUQr7bjq3WKBDEkymdCYS7ck5XVsBzBGhnEQdhh7HJ', 'status': 400}, 'http://localhost:9984/api/v1/transactions/')
```
