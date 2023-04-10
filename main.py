from code import app
from reset import reset

if __name__ == "__main__":
    # Run the bot and the reset command handler
    with app:
        app.run()
        reset.start()
    # Use Ctrl+C to stop the bot
