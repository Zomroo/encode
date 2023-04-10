from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from config import BOT_TOKEN, AUTHORIZED_USERS

# Define the /reset command handler
def reset(update, context):
    if update.message.from_user.id in AUTHORIZED_USERS:
        # Only authorized users can execute this command
        db.drop_database('mydatabase')
        update.message.reply_text('Database reset successful.')
    else:
        # Ignore the command from unauthorized users
        update.message.reply_text('You are not authorized to use this command.')

if __name__ == "__main__":
 
