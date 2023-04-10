import schedule
import time
from telegram.ext import Dispatcher

from code import updater, get_handlers

# Create a Dispatcher object and pass in the updater's bot
dispatcher = Dispatcher(updater.bot, None)

# Add the command handlers from code.py to the dispatcher
for handler in get_handlers():
    dispatcher.add_handler(handler)

# Schedule the database reset
def reset_database():
    db = Database()
    db.client.drop_database(db.db.name)
    print("Database reset.")

schedule.every().day.at("00:00").do(reset_database)

# Add the reset command handler	
dispatcher.add_handler(reset_handler)

# Start the bot
updater.start_polling()

# Start the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)

# Run the bot until interrupted
updater.idle()
