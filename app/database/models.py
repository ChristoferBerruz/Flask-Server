from pony.orm import Database, PrimaryKey, Set, Required
from datetime import datetime

## The database instance needs to be located with the models
db = Database()

class Admin(db.Entity):
    id = PrimaryKey(int, auto=True)
    firstname = Required(str)
    lastname = Required(str)
    organization = Required(str)
    email = Required(str)
    devices = Set('RecordingDevice')
    password = Required(str)

class RecordingDevice(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    location = Required(str)
    date_installed = Required(datetime)
    admin = Required(Admin)
    records = Set('HandwashingRecord')

class HandwashingRecord(db.Entity):
    id = PrimaryKey(int, auto=True)
    timestamp = Required(datetime)
    duration = Required(float)
    device = Required(RecordingDevice)
