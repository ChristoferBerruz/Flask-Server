# Configuration objects depending on environment to run


import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

JWT_SKEY = os.environ.get("SECRET_KEY")

'''
Base configuration to be extended by all other configurations
'''
class BaseConfig():
    API_PREFIX = '/api/v1'
    SECRET_KEY = JWT_SKEY
    TESTING = False
    DEBUG = False


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'