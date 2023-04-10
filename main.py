from Code import app
from database import connect

# Connect to the database
connect()

if __name__ == '__main__':
    app.run()
