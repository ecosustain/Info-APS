from pymongo import MongoClient
import os
# client = MongoClient('mongodb://localhost:27017/')
# db = client['sisab_v2']

client = MongoClient(os.getenv('DATABASE_URL'))
db = client[os.getenv('DATABASE_NAME')]