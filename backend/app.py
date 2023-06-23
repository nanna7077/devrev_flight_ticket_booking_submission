import os
import json

from flask import Flask
from flask_cors import CORS

from werkzeug.exceptions import HTTPException

from models import db

# Import the blueprints

from user_management.create import user_management_create
from user_management.read import user_management_read

from flights.create import flights_create
from flights.read import flights_read
from flights.delete import flights_delete

from tickets.create import tickets_create
from tickets.read import tickets_read


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(40)
uri = os.getenv(
    "DATABASE_URL", "sqlite:///database.sqlite3"
)  # Using sqlite3 database in testing and get the database URI from the env for production.
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS from all location

# Registering the blueprints

app.register_blueprint(user_management_create)
app.register_blueprint(user_management_read)

app.register_blueprint(flights_create)
app.register_blueprint(flights_read)
app.register_blueprint(flights_delete)

app.register_blueprint(tickets_create)
app.register_blueprint(tickets_read)

# Error handling:
# Convert all errors into JSON for easier parsing in the frontend as Flask sends a HTML page by default.

@app.errorhandler(HTTPException)
def handleOtherErrors(error):
    response = error.get_response()
    response.data = json.dumps({"error": error.description})
    response.content_type = "application/json"
    return response


# Simple index route to check if the server is running

@app.route("/")
def index():
    """
    This is the index page.
    """
    return {"message": "Hello World!"}, 200


# The application is not recommended to be run directly, but rather through waitress.
# This is because Flask's built-in server is not suitable for production.
# Still, we will be using it for testing purposes as it is easier to debug with the built-in server.

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")