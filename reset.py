import os

from pyrogram import Client, filters
from pyrogram.types import Message

from config import API_ID, API_HASH, BOT_TOKEN, MONGODB_URI, MONGODB_NAME, AUTHORIZED_USERS
from database import Database

# Create a Pyrogram client and pass in the bot's token
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Define the reset command handler
@app.on_message(filters.command('reset') & filters.user(AUTHORIZED_USERS))
def reset_command_handler(client, message):
    # Check if the user is authorized to use this command
    if message.from_user.id not in AUTHORIZED_USERS:
        return

    # Delete the entire database
    db = Database(uri=MONGODB_URI, name=MONGODB_NAME)
    db.drop_collection(MONGO_COLLECTION_NAME)

    # Send a message to confirm that the database has been deleted
    client.send_message(chat_id=message.chat.id, text="The database has been deleted.")


if __name__ == "__main__":
    # Start the bot
    app.run()
