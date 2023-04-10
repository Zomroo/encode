import os
import uuid
from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from config import BOT_TOKEN, MONGO_URL

# Set up the MongoDB database connection
db = Database(MONGO_URL)

# Create the Pyrogram bot client
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Add handler for the /en command
@bot.on_message(filters.command("en"))
def save_image(client, message):
    # Check if the message has an image
    if not message.photo:
        return

    # Save the image to MongoDB
    file_id = message.photo[-1].file_id
    unique_id = uuid.uuid4().hex[:7]
    db.collection.insert_one({"file_id": file_id, "unique_id": unique_id})

    # Send the user a reply with the unique ID
    message.reply_text(f"Image saved with ID {unique_id}")

# Add handler for the /dy command
@bot.on_message(filters.command("dy"))
def get_image(client, message):
    # Ask the user for the unique ID
    message.reply_text("Please enter the unique ID:")

@bot.on_message(filters.text)
def send_image(client, message):
    # Check if the message is a valid unique ID
    unique_id = message.text.strip()
    record = db.collection.find_one({"unique_id": unique_id})
    if not record:
        message.reply_text("Invalid unique ID")
        return

    # Get the image file ID from MongoDB and send it to the user
    file_id = record["file_id"]
    file_path = client.download_media(file_id)
    message.reply_photo(photo=open(file_path, "rb"))

    # Delete the temporary file
    os.remove(file_path)

if __name__ == "__main__":
    # Run the bot
    bot.run()
