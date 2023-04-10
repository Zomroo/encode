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




# Define the handler function for /dy command
@app.on_message(filters.command("dy"))
def handle_dy_command(bot, message):
    # Check if the user replied with an image
    if message.reply_to_message and message.reply_to_message.photo:
        # Ask the user for the 7-digit code
        bot.send_message(message.chat.id, "Please enter the 7-digit code:")
        # Use the app.ask_question method to ask the user for the code
        app.ask_question(
            chat_id=message.chat.id,
            text="Please enter the 7-digit code:",
            reply_markup=None,
            timeout=30,
            answer_cb=handle_code_input
        )
    else:
        bot.send_message(message.chat.id, "Please reply with an image to use this command.")

# Define the callback function for the code input
def handle_code_input(client, message):
    code = message.text.strip()
    if len(code) == 7 and code.isdigit():
        # Look up the code in the database
        result = collection.find_one({"code": code})
        if result and result["image_url"]:
            # Send the image to the user
            client.send_photo(message.chat.id, result["image_url"])
        else:
            client.send_message(message.chat.id, "Code not found.")
    else:
        client.send_message(message.chat.id, "Invalid code format. Please enter a 7-digit number.")




if __name__ == "__main__":
    # Start the bot
    app.run() 
