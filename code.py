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
    client.send_photo(chat_id=message.chat.id, photo=file_id, caption=f"Your photo ID is ` <code>{photo_id}</code>`", parse_mode='HTML')



# Define the dy command handler
@app.on_message(filters.command('dy'))
def dy_command_handler(client, message):
    # Ask the user for the image ID
    client.send_message(chat_id=message.chat.id, text="Please enter the image ID:")

    # Start the message handler
    @app.on_message(filters.text & ~filters.command)
    def message_handler(client, message):
        # Get the image ID from the message text
        image_id = message.text

        # Look up the image in MongoDB
        db = Database()
        image = db.find_document_by_id("images", image_id)

        # Check if the image exists
        if not image:
            client.send_message(chat_id=message.chat.id, text="Image not found. Please enter a valid image ID.")
            return

        # Send the image to the user
        client.send_photo(chat_id=message.chat.id, photo=image["file_id"], caption=f"Image ID: <code>{image_id}</code>", parse_mode='HTML')

        # End the conversation
        app.remove_handler(message_handler)

    app.add_handler(message_handler)


if __name__ == "__main__":
    # Start the bot
    app.run() 
