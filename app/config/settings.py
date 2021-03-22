# Configuration objects depending on environment to run


'''
Base configuration to be extended by all other configurations
'''
class BaseConfig():
    API_PREFIX = '/api/v1'
    TESTING = False
    DEBUG = False


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'