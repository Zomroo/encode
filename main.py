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
    file_path = '/home/gokuinstu2/encode/photo_2023-04-11_04-36-01 (1).jpg'
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

# Define the /reset command handler
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

        
MAX_IMAGES = 20

@Client.on_message(filters.command("zip"))
async def zip_command_handler(client: Client, message: Message):
    await message.reply_text("Please send the images you want to zip (max 20).")

    images = []

    # wait for the user to send images
    for i in range(MAX_IMAGES):
        response = await app.listen(message.chat.id, timeout=60)

        if response.photo:
            images.append(response.photo.file_id)
        else:
            break

    # check if any images were sent
    if not images:
        await message.reply_text("No images were sent.")
        return

    # ask the user to set a password for the zip file
    await message.reply_text("Please set a password for the zip file.")

    # wait for the user to send the password
    response = await client.listen(message.chat.id, timeout=60)

    password = response.text.strip()

    # create the zip file and encrypt it with the user's password
    zip_file = f"{message.chat.id}.zip"
    with ZipFile(zip_file, "w", compression=ZIP_DEFLATED) as zf:
        for i, image in enumerate(images):
            file_path = f"{i}.jpg"
            file_bytes = await client.download_media(image)
            zf.writestr(file_path, file_bytes)

    with ZipFile(zip_file, "r") as zf:
        zf.setpassword(password.encode("utf-8"))

    # send the zip file to the user
    await client.send_document(
        message.chat.id,
        document=zip_file,
        caption="Here is your zip file with encrypted password."
    )

    # delete the zip file from disk
    os.remove(zip_file)
        
if __name__ == "__main__":
    print("Start the bot")
    Client.run()
