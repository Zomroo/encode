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

    def update_document(self, collection_name, filter, update):
        collection = self.db[collection_name]
        result = collection.update_one(filter, update)
        return result

    def drop_database(self):
        self.client.drop_database(self.db.name)

    def get_images_from_batch(self, batch_id):
        collection = self.db['images']
        images = collection.find({'batch_id': batch_id})
        return images
