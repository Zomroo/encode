import schedule
import time

from telegram.ext import Updater, CommandHandler
from database import Database
from config import BOT_TOKEN
from code import start_handler, en_handler, dy_handler


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
start_handler = CommandHandler("start", start_command_handler)
en_handler = CommandHandler("en", en_command_handler, filters=Filters.reply)
dy_handler = CommandHandler("dy", dy_command_handler)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(en_handler)
dispatcher.add_handler(dy_handler)
dispatcher.add_handler(reset_handler)

# Schedule the database reset
def reset_database():
    db = Database()
    db.client.drop_database(db.db.name)
    print("Database reset.")

schedule.every().day.at("00:00").do(reset_database)

if __name__ == "__main__":
    # Start the main bot
    updater.start_polling()

    # Add the handlers from code.py to the main bot
    for handler in get_handlers():
        dispatcher.add_handler(handler)

    while True:
        schedule.run_pending()
        time.sleep(1)
