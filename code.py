import os
import re
import uuid

from pyrogram import Client, filters
from pyrogram.types import Message

from config import API_ID, API_HASH, BOT_TOKEN
from database import Database

# Create a Pyrogram client and pass in the bot's token
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Define the start command handler
@app.on_message(filters.command('start'))
def start_command_handler(client, message):
    client.send_message(chat_id=message.chat.id, text="Welcome to my bot!")


# Define the en command handler
@app.on_message(filters.reply & filters.command('en'))
def en_command_handler(client, message):
    # Check if the reply message is a photo message
    if not message.reply_to_message or not message.reply_to_message.photo:
        client.send_message(chat_id=message.chat.id, text="Please reply with a photo.")
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
    client.send_message(chat_id=message.chat.id, text=f"Your photo has been saved with ID {photo_id}.")




# Define a command handler that asks for a code
@app.on_message(filters.command("dy"))
def ask_code(client, message):
    # Reply to the user with a message asking for a code
    reply_message = message.reply_text("Please enter the 7 digit unique code:")
    # Register a handler that listens for the user's response
    bot.register_next_step_handler(reply_message, lookup_image)

# Define a handler that looks up an image based on a code
def lookup_image(client, message):
    # Get the code from the user's message
    code = message.text
    # Look up the image in the database
    image = image_collection.find_one({"code": code})
    if image:
        # If the image is found, send it to the user
        bot.send_photo(message.chat.id, image["file_id"], caption=image["caption"])
    else:
        # If the code is not found, send an error message to the user
        message.reply_text("Sorry, the code you entered is invalid.")




if __name__ == "__main__":
    # Start the bot
    app.run() 
