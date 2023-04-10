from pymongo import MongoClient

class Database:
    def __init__(self, url, db_name):
        self.client = MongoClient(url)
        self.db = self.client[db_name]
        self.collection = self.db.images
