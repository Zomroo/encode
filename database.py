from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

def insert_image(image_data):
    return db.images.insert_one(image_data)

def find_image_by_id(image_id):
    return db.images.find_one({'_id': image_id})
