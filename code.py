import os
import re
import uuid

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from config import BOT_TOKEN
from database import Database

app = Client("my_bot", bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
def start_command_handler(_, message: Message):
    message.reply_text("Welcome to my bot!")


@app.on_message(filters.command("en") & filters.reply)
def en_command_handler(_, message: Message):
    # check if the reply message is an image
    if not message.reply_to_message.photo:
        message.reply_text("Please reply with an image.")
        return

    # generate a unique ID for the image
    image_id = str(uuid.uuid4())[:7]

    # save the image to MongoDB
    db = Database()
    db.insert_document("images", {"_id": image_id, "file_id": message.reply_to_message.photo.file_id})

    # send a reply to the user with the ID
    message.reply_text(f"Your image ID is {image_id}.")


@app.on_message(filters.command("dy"))
def dy_command_handler(_, message: Message):
    # ask the user for the image ID
    message.reply_text("Please enter the image ID:")

    # start the callback handler
    app.register_callback_query_handler(callback_handler, filters.regex(r'^\w{7}$'))


def callback_handler(client, callback_query: CallbackQuery):
    # get the image ID from the callback data
    image_id = callback_query.data

    # look up the image in MongoDB
    db = Database()
    image = db.find_document_by_id("images", image_id)

    # check if the image exists
    if not image:
        client.answer_callback_query(callback_query.id, text="Image not found.")
        return

    # send the image to the user
    client.send_photo(chat_id=callback_query.message.chat.id, photo=image["file_id"])

    # end the conversation
    client.answer_callback_query(callback_query.id, text="Here is your image.")


if __name__ == "__main__":
    # start the bot
    app.run()
