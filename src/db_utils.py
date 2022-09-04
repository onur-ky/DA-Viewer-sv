import os
from dotenv import load_dotenv
load_dotenv()

def get_db_connection():
    from pymongo import MongoClient
    import pymongo

    db_username = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    CONNECTION_STRING = f'mongodb+srv://{db_username}:{db_password}@{db_name}.ioivhxi.mongodb.net/?retryWrites=true&w=majority'
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client