import os
import re
import uuid
from telegram.ext import CommandHandler


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import BOT_TOKEN
from database import Database

# Create an Updater object and pass in the bot's token
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define the start command handler
def start_command_handler(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my bot!")


# Define the en command handler
def en_command_handler(update, context):
    # Check if the reply message is an image
    if not update.message.reply_to_message.photo:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please reply with an image.")
        return

    # Check if the image size is above 5MB
    file_size = update.message.reply_to_message.photo[-1].file_size
    if file_size > 5242880:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, images above 5MB are not supported.")
        return

    # Generate a unique ID for the image
    image_id = str(uuid.uuid4())[:7]

    # Save the image to MongoDB
    db = Database()
    db.insert_document("images", {"_id": image_id, "file_id": update.message.reply_to_message.photo[-1].file_id})

    # Send a reply to the user with the ID and image
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('/home/gokuinstu2/encode/photo_2022-06-29_01-39-16.jpg', 'rb'), caption=f"Your image ID is `<code>{image_id}</code>`", parse_mode='HTML')

# Define the dy command handler
def dy_command_handler(update, context):
    # Ask the user for the image ID
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter the image ID:")

    # Start the message handler
    def message_handler(update, context):
        # Get the image ID from the message text
        image_id = update.message.text

        # Look up the image in MongoDB
        db = Database()
        image = db.find_document_by_id("images", image_id)

        # Check if the image exists
        if not image:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Image not found. Please enter a valid image ID.")
            return

        # Send the image to the user
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=image["file_id"], caption=f"Image ID: <code>{image_id}</code>", parse_mode='HTML')

        # End the conversation
        updater.dispatcher.remove_handler(message_handler)

    message_handler = MessageHandler(Filters.text & (~Filters.command), message_handler)
    updater.dispatcher.add_handler(message_handler)



def add_handlers(dispatcher):
    # Add handlers for the start, en, and dy commands
    dispatcher.add_handler(CommandHandler("start", start_command_handler))
    dispatcher.add_handler(CommandHandler("en", en_command_handler, filters=Filters.reply))
    dispatcher.add_handler(CommandHandler("dy", dy_command_handler))


if __name__ == "__main__":
    # Create an Updater object and pass in the bot's token
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers to the dispatcher
    add_handlers(dispatcher)

    # Start the bot
    updater.start_polling()
    updater.idle()
