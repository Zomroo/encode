import os
import re
import uuid

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

    # Generate a unique ID for the image
    image_id = str(uuid.uuid4())[:7]

    # Save the image to MongoDB
    db = Database()
    db.insert_document("images", {"_id": image_id, "file_id": update.message.reply_to_message.photo[-1].file_id})

    # Send a reply to the user with the ID
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your image ID is {image_id}.")


# Define the dy command handler
def dy_command_handler(update, context):
    # Ask the user for the image ID
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter the image ID:")

    # Start the callback handler
    def callback_handler(update, context):
        query = update.callback_query
        # Get the image ID from the callback data
        image_id = query.data

        # Look up the image in MongoDB
        db = Database()
        image = db.find_document_by_id("images", image_id)

        # Check if the image exists
        if not image:
            context.bot.answer_callback_query(callback_query_id=query.id, text="Image not found.")
            return

        # Send the image to the user
        context.bot.send_photo(chat_id=query.message.chat_id, photo=image["file_id"])

        # End the conversation
        context.bot.answer_callback_query(callback_query_id=query.id, text="Here is your image.")

    callback_handler = CallbackQueryHandler(callback_handler, pattern='^\\w{7}$')
    dispatcher.add_handler(callback_handler)


# Add handlers for the start, en and dy commands
start_handler = CommandHandler("start", start_command_handler)
en_handler = CommandHandler("en", en_command_handler, filters=Filters.reply)
dy_handler = CommandHandler("dy", dy_command_handler)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(en_handler)
dispatcher.add_handler(dy_handler)


if __name__ == "__main__":
    # Start the bot
    updater.start_polling()
    updater.idle()
