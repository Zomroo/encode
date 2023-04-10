import os
import re
import uuid
import schedule
import time

from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from config import API_ID, API_HASH, BOT_TOKEN
from database import Database

# Create a Pyrogram client and pass in the bot's token
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Define the start command handler
@app.on_message(filters.command('start'))
def start_command_handler(client, message):
    client.send_message(chat_id=message.chat.id, text="Welcome to my bot!")


# Define the en command handler
@app.on_message(filters.command('en'))
def en_command_handler(client, message):
    # Check if the user has replied to an image message
    if message.reply_to_message is None or message.reply_to_message.photo is None:
        client.send_message(chat_id=message.chat.id, text="Please reply to a photo message with /en.")
        return

    # Get the photo file ID and size
    photo = message.reply_to_message.photo
    file_id = photo.file_id
    file_size = photo.file_size

    # Check if the photo size is above 5MB
    if file_size > 5242880:
        client.send_message(chat_id=message.chat.id, text="Sorry, photos above 5MB are not supported.")
        return

    # Generate a unique ID for the photo
    photo_id = str(uuid.uuid4())[:7]

    # Save the photo to MongoDB
    db = Database()
    db.insert_document("photos", {"_id": photo_id, "file_id": file_id})

    # Send a reply to the user with the ID and photo
    file_path = '/home/gokuinstu2/encode/photo_2023-04-11_04-36-01 (1).jpg'
    client.send_photo(chat_id=message.chat.id, photo=file_path, caption=f"Your photo has been saved with ID `{photo_id}`.")


# Define the /dy command handler
@app.on_message(filters.command('dy'))
def dy_command_handler(client, message):
    # Check if the reply message is a photo message
    if not message.reply_to_message or not message.reply_to_message.photo:
        client.send_message(chat_id=message.chat.id, text="Please reply with a photo.")
        return

    # Check if the photo has the required dimensions
    photo = message.reply_to_message.photo
    file_id = photo.get_biggest().file_id

    if photo.width != 1279 or photo.height != 1279:
        client.send_message(chat_id=message.chat.id, text="Please reply with a photo that is 1279x1279.")
        return
    # Ask the user for an ID
    client.send_message(chat_id=message.chat.id, text="Please enter the ID:")

    # Wait for a reply from the user
    @app.on_message(filters.chat(message.chat.id) & filters.text)
    def handle_reply(client, reply):
        # Check if the reply message is from the same user and is a text message
        if reply.from_user.id == message.from_user.id and reply.text:
            # Get the ID from the reply
            id = reply.text.strip()

            # Look up the image in MongoDB
            db = Database()
            image = db.get_document("photos", {"_id": id})

            # If the image exists, send it to the user
            if image and "file_id" in image:
                client.send_photo(chat_id=message.chat.id, photo=image["file_id"])
            else:
                # If the image does not exist, send an error message
                client.send_message(chat_id=message.chat.id, text="Image not found.")

            # Remove the reply handler
            app.remove_handler(handle_reply)

    # Add the reply handler to the bot's handlers
    app.add_handler(handle_reply)


# Define the reset command handler
@app.on_message(filters.command('reset'))
def reset_command_handler(client, message):
    # Check if the user is authorized
    if message.from_user.id not in [5148561602]: # Replace with authorized user IDs
        return

    # Reset the database and send a confirmation message
    if reset_database():
        client.send_message(chat_id=message.chat.id, text="Database reset successfully.")
    else:
        client.send_message(chat_id=message.chat.id, text="Failed to reset database.")

def reset_database():
    try:
        # Connect to the MongoDB database
        client = MongoClient("mongodb+srv://Zoro:Zoro@cluster0.x1vigdr.mongodb.net/?retryWrites=true&w=majority")
        db = client["telegram_bot"]
        
        # Delete all documents in each collection
        for name in db.list_collection_names():
            db[name].delete_many({})
        
        # Set up TTL (time-to-live) index to delete documents after 24 hours
        db.photos.create_index("created_at", expireAfterSeconds=24*60*60)
        
        client.close()
        return True
    except ConnectionFailure:
        return False

# Define the /reset command handler
@app.on_message(filters.command('reset'))
def reset_command_handler(client, message):
    # Check if the user is authorized
    if message.from_user.id not in [5148561602]: # Replace with authorized user IDs
        return
    # Reset the database and send a confirmation message
    if reset_database():
        client.send_message(chat_id=message.chat.id, text="Database reset successfully.")
    else:
        client.send_message(chat_id=message.chat.id, text="Failed to reset database.")

if __name__ == "__main__":
    # Start the bot
    app.run()
