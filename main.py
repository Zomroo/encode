import os
import re
import uuid
import schedule
import time

from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from zipfile import ZipFile, ZIP_DEFLATED
from pymongo.errors import ConnectionFailure

from database import Database

from config import *

Client = Client('sex-bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define the /zip command handler
@Client.on_message(filters.command('zip'))
def zip_command_handler(client, message):
    # Ask the user to send photos
    client.send_message(chat_id=message.chat.id, text="Please send me up to 20 photos to zip.")
    
    # Define a dictionary to store the photos
    photos = {}

    # Define the handle_photos function
    @Client.on_message(filters.chat(message.chat.id) & filters.photo & ~filters.edited_message)
    def handle_photos(client, message):
        # Check if the maximum number of photos has been reached
        if len(photos) >= 20:
            client.send_message(chat_id=message.chat.id, text="Maximum number of photos reached.")
            Client.remove_handler(handle_photos)
            return

        # Add the photo to the dictionary
        photos[message.message_id] = message.photo.file_id
        client.send_message(chat_id=message.chat.id, text=f"{len(photos)} photo(s) added. Please send more or enter /done to zip.")

    # Add the photos handler to the bot's handlers
    Client.add_handler(handle_photos)
    
    # Define the done_command_handler function
    @Client.on_message(filters.command('done'))
    def done_command_handler(client, message):
        # Check if there are any photos to zip
        if not photos:
            client.send_message(chat_id=message.chat.id, text="No photos to zip.")
            Client.remove_handler(handle_photos)
            Client.remove_handler(done_command_handler)
            return

        # Ask the user to set a password for the zip file
        client.send_message(chat_id=message.chat.id, text="Please set a password for the zip file.")

        # Define the handle_password function
        @Client.on_message(filters.chat(message.chat.id) & filters.text)
        def handle_password(client, reply):
            # Check if the reply message is from the same user and is a text message
            if reply.from_user.id == message.from_user.id and reply.text:
                # Get the password from the reply
                password = reply.text.strip()

                # Create a zip file with the photos
                zip_file_name = str(uuid.uuid4()) + ".zip"
                with ZipFile(zip_file_name, "w", ZIP_DEFLATED) as zip_file:
                    for message_id, file_id in photos.items():
                        # Download the photo file
                        file_path = client.download_media(file_id)

                        # Add the photo file to the zip file
                        zip_file.write(file_path, os.path.basename(file_path))

                        # Delete the photo file
                        os.remove(file_path)

                # Encrypt the zip file with the password
                encrypted_zip_file_name = zip_file_name + ".enc"
                os.system(f"zip -r -P {password} {encrypted_zip_file_name} {zip_file_name}")
                os.remove(zip_file_name)

                # Send the encrypted zip file to the user
                client.send_document(chat_id=message.chat.id, document=encrypted_zip_file_name)

                # Remove the handlers
                Client.remove_handler(handle_photos)
                Client.remove_handler(handle_password)

        # Add the password handler to the bot's handlers
        Client.add_handler(handle_password)

# Define the start command handler
@Client.on_message(filters.command('start'))
def start_command_handler(client, message):
    client.send_message(chat_id=message.chat.id, text="Welcome to my bot!")


# Define the en command handler
@Client.on_message(filters.command('en'))
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
    file_path = '/root/encode/photo_2023-04-11_04-36-01 (1).jpg'
    client.send_photo(chat_id=message.chat.id, photo=file_path, caption=f"Your photo has been saved with ID `{photo_id}`.")


# Define the /dy command handler
@Client.on_message(filters.command('dy'))
def dy_command_handler(client, message):
    # Check if the reply message is a photo message
    if not message.reply_to_message or not message.reply_to_message.photo:
        client.send_message(chat_id=message.chat.id, text="Please reply with a photo.")
        return

    # Check if the photo has the required dimensions
    photo = message.reply_to_message.photo
    file_id = photo.file_id

    if photo.width != 1279 or photo.height != 1279:
        client.send_message(chat_id=message.chat.id, text="Please reply with a photo that is encoded.")
        return

    # Ask the user for an ID
    client.send_message(chat_id=message.chat.id, text="Please enter the ID:")

    # Wait for a reply from the user
    @Client.on_message(filters.chat(message.chat.id) & filters.text)
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
            Client.remove_handler(handle_reply)

    # Add the reply handler to the bot's handlers
    Client.add_handler(handle_reply)


# Define the reset command handler
@Client.on_message(filters.command('reset'))
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


        
if __name__ == "__main__":
    print("Start the bot")
    Client.run()
