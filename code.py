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

    # create an inline keyboard with a "Cancel" button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ])

    # send the message with the keyboard
    app.send_message(
        chat_id=message.chat.id,
        text="Please enter the image ID:",
        reply_markup=keyboard
    )


    # set the next handler to get the image ID from the user
    app.register_callback_query_handler(handle_image_id_1, message.chat.id)


def handle_image_id_1(_, query: CallbackQuery):
    # check if the callback query data is "cancel"
    if query.data == "cancel":
        query.message.reply_text("Cancelled.")
        return

    # get the image ID from the callback query data
    image_id = query.data

    # look up the image in MongoDB
    db = Database()
    image = db.find_document_by_id("images", image_id)

    # check if the image exists
    if not image:
        query.answer("Image not found.", show_alert=True)
        return

    # send the image to the user
    query.message.reply_photo(photo=image["file_id"])


@app.on_callback_query()
def handle_callback_query(_, query: CallbackQuery):
    # get the image ID from the callback data
    image_id = query.data.strip()

    # look up the image in MongoDB
    db = Database()
    image = db.find_document_by_id("images", image_id)

    # check if the image exists
    if not image:
        query.answer("Image not found.", show_alert=True)
        return

    # send the image to the user
    query.message.reply_photo(photo=image["file_id"])


if __name__ == "__main__":
    # start the bot
    app.run()
