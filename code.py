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




@app.on_message(filters.command(['dy']) & filters.photo)
def handle_command(client, message):
    # Ask for 7-digit unique code
    client.send_message(chat_id=message.chat.id, text='Please enter 7-digit unique code:')
    # Set a filter to wait for the user's response
    app.on_message(filters.private & filters.text)(ask_code)
# Define a function to handle user's code input
def ask_code(client, message):
    # Check if the message contains a 7-digit unique code
    code = message.text.strip()
    if len(code) != 7 or not code.isdigit():
        client.send_message(chat_id=message.chat.id, text='Invalid code. Please enter a 7-digit unique code.')
        return

    # Search for the code in MongoDB
    db = Database()
    result = db.find_document("photos", {"_id": code})

    if result:
        # Send the corresponding image to the user
        client.send_photo(chat_id=message.chat.id, photo=result['file_id'])
    else:
        client.send_message(chat_id=message.chat.id, text='Code not found.')





if __name__ == "__main__":
    # Start the bot
    app.run() 
