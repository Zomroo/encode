import schedule
import time

from telegram.ext import CommandHandler
from telegram.ext import Updater
from code import updater
from batch import batch_command_handler
from reset import reset_handler
from database import Database

# Create an Updater object and pass it your bot's token
updater = Updater(token='YOUR_TOKEN_HERE', use_context=True)

# Get the dispatcher object from the updater
dispatcher = updater.dispatcher

def reset_database():
    db = Database()
    db.client.drop_database(db.db.name)
    print("Database reset.")

if __name__ == "__main__":
    # start the bot
    updater.start_polling()

    # schedule the database reset
    schedule.every().day.at("00:00").do(reset_database)
    
    # Define the /batch command handler
    batch_handler = CommandHandler("batch", batch_command_handler)
    dispatcher.add_handler(batch_handler)
    
    
    
    dispatcher.add_handler(CommandHandler('batch', batch_command_handler))
    dispatcher.add_handler(CommandHandler('done', done_command_handler))
    dispatcher.add_handler(CommandHandler('dy', dy_command_handler))
    dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
   

    # add the reset command handler
    updater.dispatcher.add_handler(reset_handler)

    while True:
        schedule.run_pending()
        time.sleep(1)
