from pyrogram import Client, filters
from pyrogram.types import Message
from database import Database
from config import BOT_TOKEN, AUTHORIZED_USERS

# Create a Pyrogram client and pass in the bot's token
app = Client(
    "my_bot",
    bot_token=BOT_TOKEN,
    workers=1
)

# Define the reset command handler
@app.on_message(filters.command("reset") & filters.user(AUTHORIZED_USERS))
def reset_command_handler(client, message):
    # Check if the user is authorized to use this command
    if message.from_user.id not in AUTHORIZED_USERS:
        return

    # Reset the database
    db = Database()
    db.client.drop_database(db.db.name)

    # Send a message to confirm that the database has been reset
    client.send_message(
        chat_id=message.chat.id,
        text="Database reset."
    )

if __name__ == "__main__":
    # Start the bot
    app.run()
