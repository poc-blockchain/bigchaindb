# Vehicle Management

## Set up local development

### Install pipenv

``` bash
brew install pipenv
```

### Setup virtual env

``` bash
cd vehicle-management
./pyenv.sh
```

### Instal dependencies

``` bash
pipenv install
```

### Run the demo on jupyter

``` bash
cd src
jupyter notebook
```

Open the demo.ipynb then execute.

### Error when commit a transaction on MacOS

``` text
ssl.SSLError: [SSL: TLSV1_ALERT_PROTOCOL_VERSION] tlsv1
```

On MacOS run pip install pip install 'requests[security]'
