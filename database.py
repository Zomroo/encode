import datetime
import pytz
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME


class Database:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]
        self.collection = self.db[MONGO_COLLECTION_NAME]
    
    def add_image(self, file_id):
        return str(self.collection.insert_one({"file_id": file_id}).inserted_id)
    
    def get_image_by_id(self, image_id):
        return self.collection.find_one({"_id": ObjectId(image_id)})
    
    def reset(self):
        self.collection.drop()
    
    def schedule_reset(self):
        tz = pytz.timezone("UTC")
        now = datetime.datetime.now(tz)
        tomorrow = now + datetime.timedelta(days=1)
        tomorrow = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0, 0, tz)
        delta = tomorrow - now
        delta_seconds = delta.total_seconds()
        return delta_seconds
