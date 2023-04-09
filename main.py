import schedule
import time

from telegram.ext import Updater, CommandHandler
from database import Database
from config import BOT_TOKEN

# Create an Updater object and pass in the bot's token
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define the reset command handler
def reset_command_handler(update, context):
    db = Database()
    db.client.drop_database(db.db.name)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Database reset.")

# Add the reset command handler to the main bot
reset_handler = CommandHandler("reset", reset_command_handler)
dispatcher.add_handler(reset_handler)

# Start the main bot
updater.start_polling()

# Schedule the database reset
def reset_database():
    db = Database()
    db.client.drop_database(db.db.name)
    print("Database reset.")

schedule.every().day.at("00:00").do(reset_database)

while True:
    schedule.run_pending()
    time.sleep(1)
