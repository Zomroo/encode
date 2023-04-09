import uuid
import logging

from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import ChatAction

from database import Database

logger = logging.getLogger(__name__)

# Define a function to handle the /batch command
def batch_command_handler(update, context):
    # Reply to the user with instructions on how to send images
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Please send me up to 10 images.\n"
                                  "When you're done, type /done to save the images.")

    # Set the user's state to expecting images
    context.user_data['batch_state'] = 'expecting_images'

    return

# Define a function to handle images sent by the user
def image_handler(update, context):
    # Get the user's current state
    state = context.user_data.get('batch_state')

    if state == 'expecting_images':
        # Check if the user has already sent 10 images
        if 'images' not in context.user_data:
            context.user_data['images'] = []

        if len(context.user_data['images']) >= 10:
            context.bot.send_message(chat_id=update.effective_chat.id, 
                                     text="You can't send more than 10 images at a time.\n"
                                          "Please type /done to save the images you've sent.")
            return

        # Download the image file and add it to the user's list of images
        file_id = update.message.photo[-1].file_id
        file = context.bot.get_file(file_id)
        context.user_data['images'].append(file)

        # Let the user know the image has been received
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Image received.")

    else:
        # If the user is not expecting images, ignore the message
        return

# Define a function to handle the /done command
def done_command_handler(update, context):
    # Check if the user has sent any images
    if 'images' not in context.user_data or len(context.user_data['images']) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="You haven't sent me any images.\n"
                                      "Please type /batch to start a new batch.")
        return

    # Generate a unique batch ID
    batch_id = str(uuid.uuid4())

    # Save the images to the database
    db = Database()
    db.add_images_to_batch(batch_id, context.user_data['images'])

    # Clear the user's batch state and image list
    context.user_data.clear()

    # Let the user know the images have been saved and provide the batch ID
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=f"Images saved with batch ID {batch_id}.\n"
                                  f"Type /dy {batch_id} to get the images.")

    return

# Define a function to handle the /dy command
def dy_command_handler(update, context):
    # Parse the batch ID from the command
    try:
        batch_id = context.args[0]
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="Please provide a batch ID.")
        return

    # Get the images from the database
db = Database()
images = db.get_images_from_batch(batch_id)

if images is None:
    # If no images were found, let the user know
    context.bot.send_message(chat_id=update.effective_chat.id, text="No images found for this batch ID.")
else:
    # Create a new list to store the image file IDs
    file_ids = []

    # Loop through the images and add them to the list
    for image in images:
        file_ids.append(image["file_id"])

    # Send the images to the user
    context.bot.send_media_group(chat_id=update.effective_chat.id, media=[InputMediaPhoto(file_id) for file_id in file_ids])

