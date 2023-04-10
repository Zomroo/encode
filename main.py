import schedule
import time

from code import updater, start_handler, en_handler, dy_handler
from reset import reset_handler	
from batch import dispatcher	
from database import Database


def reset_database():
    db = Database()
    db.client.drop_database(db.db.name)
    print("Database reset.")

if __name__ == "__main__":
    # start the bot
    updater.start_polling()

    # add the command handlers from code.py
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(en_handler)
    updater.dispatcher.add_handler(dy_handler)
    
    # add the reset command handler
    updater.dispatcher.add_handler(reset_handler)

    # schedule the database reset
    schedule.every().day.at("00:00").do(reset_database)

    # start the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)

    # run the bot until interrupted
    updater.idle()
