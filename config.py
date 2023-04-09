import os

# Telegram API credentials
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

# Telegram Bot API token
TOKEN = os.environ.get("TOKEN")

# MongoDB connection settings
MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB_NAME = "telegram_bot"
MONGO_COLLECTION_NAME = "images"
