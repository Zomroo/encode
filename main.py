import schedule
import time

from code import updater
from database import Database
from reset import updater as reset_updater

# start the reset bot to register the reset command
reset_updater.start_polling()

def reset_database():
    db = Database()
    db.client.drop_database(db.db.name)
    print("Database reset.")


if __name__ == "__main__":
    # start the main bot
    updater.start_polling()

    # schedule the database reset
    schedule.every().day.at("00:00").do(reset_database)

    while True:
        schedule.run_pending()
        time.sleep(1)
