import schedule
import time

from code import updater
from reset import reset_handler, updater as reset_updater
from database import Database

# Start the main bot
updater.start_polling()

# Define the reset database function
def reset_database():
    db = Database()
    db.client.drop_database(db.db.name)
    print("Database reset.")

# Schedule the database reset
schedule.every().day.at("00:00").do(reset_database)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
    
    # Check for the "/reset" command
    updates = reset_updater.polling_queue.get()
    for update in updates:
        reset_handler(update, reset_updater)
