import os

# Telegram API credentials
API_ID = int(os.environ.get("16844842"))
API_HASH = os.environ.get("f6b0ceec5535804be7a56ac71d08a5d4")

# Telegram Bot API token
TOKEN = os.environ.get("5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk")

# MongoDB connection settings
MONGO_URI = os.environ.get("mongodb+srv://Zoro:<password>@cluster0.x1vigdr.mongodb.net/?retryWrites=true&w=majority")
MONGO_DB_NAME = "telegram_bot"
MONGO_COLLECTION_NAME = "images"
