import schedule
import time

from code import updater as code_updater
from telegram.ext import CommandHandler
from batch import dispatcher as batch_dispatcher
from reset import reset_handler
from database import Database

def reset_database():
    db = Database()
    db.client.drop_database(db.db.name)
    print("Database reset.")

if __name__ == "__main__":
    # start the bot
    code_updater.start_polling()

    # schedule the database reset
    schedule.every().day.at("00:00").do(reset_database)

    # add the reset command handler
    code_updater.dispatcher.add_handler(reset_handler)

    # add the batch handlers to the batch dispatcher
    batch_dispatcher.add_handler(CommandHandler('batch', batch_command_handler))
    batch_dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
    batch_dispatcher.add_handler(CommandHandler('done', done_command_handler))
    batch_dispatcher.add_handler(CommandHandler('dby', dby_command_handler))

    while True:
        schedule.run_pending()
        time.sleep(1)
