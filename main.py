from code import app
from reset import reset_app
import config

if __name__ == "__main__":
    # Run the bot and the reset command handler
    app.start()
    reset_app.start()
    # Use Ctrl+C to stop the bot
