from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()
import argparse
import json

def get_db_connection():
    from pymongo import MongoClient
    import pymongo

    db_username = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    CONNECTION_STRING = f'mongodb+srv://{db_username}:{db_password}@{db_name}.ioivhxi.mongodb.net/?retryWrites=true&w=majority'
    client = pymongo.MongoClient(CONNECTION_STRING)
    return client

def populate_db(pathway_name, data_path):
    db = get_db_connection()
    for i, fname in enumerate(os.listdir(data_path)):
        print(f'{fname}: {i+1}/{len(os.listdir(data_path))}')
        annofile = open(os.path.join(data_path, fname))
        annodata = json.load(annofile)
        db['pathways'][pathway_name].insert_one({'group': fname.split('.')[0], 'annotation': annodata})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dpath', type=str)
    parser.add_argument('--tag', type=str)
    args = parser.parse_args()
    populate_db(args.tag, args.dpath)


if __name__ == '__main__':
    main()
