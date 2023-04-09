import schedule
import time
import psutil

from code import updater
from database import Database
from reset import updater as reset_updater

def is_running(process):
    for proc in psutil.process_iter():
        try:
            if process.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def reset_database():
    db = Database()
    db.client.drop_database(db.db.name)
    print("Database reset.")

if __name__ == "__main__":
    if is_running("python main.py"):
        print("Bot is already running!")
        exit(1)

    # start the reset bot to register the reset command
    reset_updater.start_polling()

    # start the main bot
    updater.start_polling()

    # schedule the database reset
    schedule.every().day.at("00:00").do(reset_database)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            break
