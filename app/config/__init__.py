import os
import sys
from app.config.settings import ProductionConfig, DevConfig

APP_ENV = os.environ.get('APP_ENV', 'Dev')


# Small switch to give config back
def get_config():

    if APP_ENV == 'Dev':
        return DevConfig()

    if APP_ENV == 'Production':
        return ProductionConfig()


# Exporting config instance
config = get_config()