# Configuration objects depending on environment to run


import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

JWT_SKEY = os.environ.get("JWT_SECRET_KEY")
DB_USER = os.environ.get("DB_USER")
DB_PORT = os.environ.get("DB_PORT")
DB_HOST = os.environ.get("DB_HOST")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
_CACHE_HOST = os.environ.get("CACHE_HOST")

provider = 'postgres'
db_name = 'postgres'

db_options=dict(
    provider=provider,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=db_name
)

'''
Base configuration to be extended by all other configurations
'''
class BaseConfig():
    API_PREFIX = '/api/v1'
    DB_OPTIONS = db_options
    CACHE_HOST = _CACHE_HOST
    SECRET_KEY = JWT_SKEY
    TESTING = False
    DEBUG = False


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'