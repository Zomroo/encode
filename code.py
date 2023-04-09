import os
import re
import uuid

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

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
    message.reply_photo(photo="husysb.png", caption=f"Your image ID is {image_id}.")


@app.on_message(filters.command("dy"))
def dy_command_handler(_, message: Message):
    # ask the user for the image ID
    message.reply_text("Please enter the image ID:")

    # set the next handler to get the image ID from the user
    app.set_callback_data_handler(handle_image_id)


def handle_image_id(_, message: Message):
    # get the image ID from the user's message
    image_id = message.text.strip()

    # check if the image ID is valid
    if not re.match(r"^[a-zA-Z0-9]{7}$", image_id):
        message.reply_text("Invalid image ID.")
        return

    # look up the image in MongoDB
    db = Database()
    image = db.find_document_by_id("images", image_id)

    # check if the image exists
    if not image:
        message.reply_text("Image not found.")
        return

    # send the image to the user
    message.reply_photo(photo=image["file_id"])


if __name__ == "__main__":
    # start the bot
    app.run()
