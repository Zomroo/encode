import schedule
import time
import uuid

from telegram.ext import CommandHandler
from code import updater, get_handlers, start_command_handler, en_command_handler, dy_command_handler
from reset import reset_handler
from batch import dispatcher
from database import Database

# Add the command handlers from code.py
dispatcher.add_handler(CommandHandler('start', start_command_handler))
dispatcher.add_handler(CommandHandler('en', en_command_handler))
dispatcher.add_handler(CommandHandler('dy', dy_command_handler))

# Add the reset command handler
dispatcher.add_handler(reset_handler)

# Schedule the database reset
def reset_database():
    db = Database()
    db.client.drop_database(db.db.name)
    print("Database reset.")

schedule.every().day.at("00:00").do(reset_database)

# Assign dispatcher before starting the updater
updater.dispatcher = dispatcher

# Start the bot
updater.start_polling()

# Start the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)

# Run the bot until interrupted
updater.idle()
