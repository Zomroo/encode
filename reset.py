from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from config import BOT_TOKEN, AUTHORIZED_USERS

# Create the Pyrogram client instance for the reset command
reset_app = Client("reset_bot", bot_token=BOT_TOKEN)

@reset_app.on_message(filters.command('reset'))
def reset_command_handler(client: Client, message: Message):
    # Ignore the command from unauthorized users
    if message.from_user.id not in AUTHORIZED_USERS:
        message.reply_text('You are not authorized to use this command.')
        return

    db.drop_database('mydatabase')
    message.reply_text('Database reset successful.')
