# Configuration objects depending on environment to run


import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

JWT_SKEY = os.environ.get("SECRET_KEY")
USER = os.environ.get("USER")
PORT = os.environ.get("PORT")
HOST = os.environ.get("HOST")
PASSWORD = os.environ.get("PASSWORD")

provider = 'postgres'
db_name = 'postgres'

db_options=dict(
    provider=provider,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    database=db_name
)

'''
Base configuration to be extended by all other configurations
'''
class BaseConfig():
    API_PREFIX = '/api/v1'
    DB_OPTIONS = db_options
    SECRET_KEY = JWT_SKEY
    TESTING = False
    DEBUG = False


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'