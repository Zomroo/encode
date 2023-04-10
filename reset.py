import os

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.contrib import MongoStorage

from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, MONGO_DB_NAME, AUTHORIZED_USERS

# Create a Pyrogram client and pass in the bot's token
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    storage=MongoStorage(
        uri=MONGO_URI,
        database_name=MONGO_DB_NAME,
        client_options={
            "retryWrites": False
        }
    )
)

# Define the reset command handler
@app.on_message(filters.command('reset') & filters.user(AUTHORIZED_USERS))
def reset_command_handler(client, message):
    # Check if the user is authorized to use this command
    if message.from_user.id not in AUTHORIZED_USERS:
        return

    # Delete the entire database
    app.storage.drop()

    # Send a message to confirm that the database has been deleted
    client.send_message(chat_id=message.chat.id, text="The database has been deleted.")


if __name__ == "__main__":
    # Start the bot
    app.run()
