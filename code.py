import os
import uuid
from pyrogram import Client, filters
from pyrogram.types import Message
from database import insert_image, find_image_by_id
from config import BOT_TOKEN

# Initialize the Telegram client
app = Client('my_bot', bot_token=BOT_TOKEN)

# Define a filter to handle messages with "/en" command
@filters.command('en')
def save_image(client, message: Message):
    # Get the user ID
    user_id = message.from_user.id
    
    # Check if the user sent an image
    if message.photo:
        # Get the file ID of the largest image
        file_id = message.photo[-1].file_id
        
        # Save the image to MongoDB
        db.images.insert_one({'user_id': user_id, 'file_id': file_id})
        
        # Generate a unique 7-digit ID for the image
        image_id = str(db.images.find().count()).zfill(7)
        
        # Send a message to the user with the image ID and image as caption
        message.reply_photo(
            photo='/home/gokuinstu2/encode/photo_2022-06-29_01-39-16.jpg',
            caption=f'Image saved with ID: {image_id}'
        )
    else:
        # Send a message to the user if they didn't send an image
        message.reply_text("Please send an image")


# Define a filter to handle messages with "/dy" command
@filters.command('dy')
def retrieve_image(client, message: Message):
    # Ask for the image ID
    message.reply_text('Please enter the ID of the image you want to retrieve.')

    # Define a callback to handle the response
    @app.on_message(filters.private & filters.text)
    def handle_image_id(_, message: Message):
        # Find the image by ID
        image_id = message.text
        image_data = find_image_by_id(image_id)

        if not image_data:
            # Reply if the ID is incorrect
            message.reply_text('The provided ID is incorrect.')
            return

        # Send the photo to the user
        file_id = image_data['file_id']
        message.reply_photo(photo=file_id)

        # Remove the callback
        app.remove_handler(handle_image_id)

# Define a filter to handle the "/start" command
@filters.command('start')
def start_command(_, message: Message):
    message.reply_text('Welcome to my bot! Use /en to save an image and /dy to retrieve it by ID.')

# Run the client
app.run()
