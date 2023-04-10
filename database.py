from pymongo import MongoClient
from config import MONGODB_URI, MONGODB_NAME
from pyrogram import Client


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

    def update_document(self, collection_name, filter, update):
        collection = self.db[collection_name]
        result = collection.update_one(filter, update)
        return result

    def get_document(self, collection_name, filter):
        collection = self.db[collection_name]
        return collection.find_one(filter)

    def drop_database(self):
        self.client.drop_database(self.db.name)


class PyrogramDatabase:
    def __init__(self, client):
        self.client = client
        self.db = MongoClient(MONGODB_URI)[MONGODB_NAME]

    async def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        return collection.insert_one(document)

    async def find_document_by_id(self, collection_name, document_id):
        collection = self.db[collection_name]
        return collection.find_one({"_id": document_id})

    async def update_document(self, collection_name, filter, update):
        collection = self.db[collection_name]
        result = collection.update_one(filter, update)
        return result

    async def get_document(self, collection_name, filter):
        collection = self.db[collection_name]
        return collection.find_one(filter)

    async def drop_database(self):
        MongoClient(MONGODB_URI).drop_database(self.db.name)
        
        from pymongo import MongoClient

def reset_db():
    with MongoClient(MONGODB_URI) as client:
        client.drop_database(MONGODB_NAME)

