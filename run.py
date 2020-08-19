from app import app
from waitress import serve

if __name__ == "__main__":
    # Use this if you're running the app on a local machine
    app.run()
    # Use this if you're running the app on a production server
    #serve(app)

