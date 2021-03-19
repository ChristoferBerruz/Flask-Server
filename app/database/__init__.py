from .models import db
from .models import Admin, HandwashingRecord, RecordingDevice
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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

def init_database():
    
    db.bind(**db_options)
    db.generate_mapping(create_tables=True)