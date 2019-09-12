import os

import pymongo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# mongo
mongo_client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
mongo_db = mongo_client.get_default_database()

# local db
db_url = os.environ.get('LOCAL_DB_URI')
local_db_engine = create_engine(db_url)
session_args = {'autocommit': False, 'autoflush': False}
session_maker = sessionmaker(bind=local_db_engine, **session_args)
