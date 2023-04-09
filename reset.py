from telegram.ext import Updater, CommandHandler
from database import Database

from config import BOT_TOKEN, AUTHORIZED_USERS


# Create an Updater object and pass in the bot's token
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define the reset command handler
def reset_command_handler(update, context):
    user_id = update.message.from_user.id
    if user_id in AUTHORIZED_USERS:
        db = Database()
        db.client.drop_database(db.db.name)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Database reset.")
    else:

# Add the reset command handler
reset_handler = CommandHandler("reset", reset_command_handler)
dispatcher.add_handler(reset_handler)

if __name__ == "__main__":
    # Start the bot
    updater.start_polling()
    updater.idle()
