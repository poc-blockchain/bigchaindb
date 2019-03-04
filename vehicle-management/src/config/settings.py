import os

from dotenv import load_dotenv

load_dotenv('./.env')

APP_NAME = os.getenv('APP_NAME')
APP_PUBLIC_KEY = os.getenv('APP_PUBLIC_KEY')
APP_PRIVATE_KEY = os.getenv('APP_PRIVATE_KEY')
