import schedule
import time

from telegram.ext import CommandHandler
from code import updater, get_handlers
from reset import reset_handler
from batch import dispatcher
from database import Database

# Add the command handlers from code.py
for handler in get_handlers():
    dispatcher.add_handler(handler)

# Add the reset command handler
dispatcher.add_handler(reset_handler)

# Schedule the database reset
def reset_database():
    db = Database()
    db.client.drop_database(db.db.name)
    print("Database reset.")

schedule.every().day.at("00:00").do(reset_database)

# Start the bot
updater.start_polling()

# Start the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)

# Run the bot until interrupted
updater.idle()
