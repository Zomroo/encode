import schedule
import time

from code import updater
from reset import updater as reset_updater  # import the reset_updater from reset.py
from database import Database

# Start the reset bot to register the reset command
reset_updater.start_polling()

# Start the main bot
updater.start_polling()

# Schedule the database reset
def reset_database():
    reset_updater.start_polling()
    db = Database()
    db.client.drop_database(db.db.name)
    reset_updater.stop()
    print("Database reset.")

schedule.every().day.at("00:00").do(reset_database)

while True:
    schedule.run_pending()
    time.sleep(1)
