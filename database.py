from pymongo import MongoClient
from config import MONGODB_URI, MONGODB_NAME

class Database:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_NAME]

    def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        return collection.insert_one(document)

    def find_document_by_id(self, collection_name, document_id):
        collection = self.db[collection_name]
        return collection.find_one({"_id": document_id})
