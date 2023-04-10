import schedule
import time

from code import updater
from reset import reset_handler
from database import Database
from batch import batch_command_handler, done_command_handler, dby_command_handler

# add the batch command handler
batch_handler = CommandHandler('batch', batch_command_handler)
updater.dispatcher.add_handler(batch_handler)

# add the done command handler
done_handler = CommandHandler('done', done_command_handler)
updater.dispatcher.add_handler(done_handler)

# add the dby command handler
dby_handler = CommandHandler('dby', dby_command_handler)
updater.dispatcher.add_handler(dby_handler)

def reset_database():
    db = Database()
    db.client.drop_database(db.db.name)
    print("Database reset.")

if __name__ == "__main__":
    # start the bot
    updater.start_polling()

    # schedule the database reset
    schedule.every().day.at("00:00").do(reset_database)

    # add the reset command handler
    updater.dispatcher.add_handler(reset_handler)

    while True:
        schedule.run_pending()
        time.sleep(1)
