from pymongo import MongoClient

class Database:
    def __init__(self, mongo_url, db_name, collection_name):
        self.client = MongoClient(mongo_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
