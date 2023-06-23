from hashlib import sha256
import re
from flask import Blueprint, request, jsonify

# We import modules and not the inner contents to prevent namespace pollution.
# i.e, we are not importing from models import * and rather are importing from models like models.User
# While this may be more verbose, it is better for code readability, maintainability and also prevents conflicts between modules.

import models
import auth
import common

user_management_create = Blueprint("user_management_create", __name__)

@user_management_create.route("/users/register", methods=["POST"])
def register():
    """
    Registers a new user.
    """
    requestdata = request.get_json(force=True)
    if not requestdata:
        return ({"error": "Invalid JSON data"}, 400)
    
    name = str(requestdata.get("name")) # User name is required to be a string.
    email = requestdata.get("email") # Email is required to be a string.
    password = str(requestdata.get("password")) # Convert to string to prevent error when encoding.

    if not name or not email or not password:
        return {"error": "Missing data"}, 400
    if not re.match(common.EMAIL_VALIDATION_PATTERN, email): # We use the common regex rather than defining it here so that we can update it in one place.
        return {"error": "Invalid email"}, 400
    if models.User.query.filter_by(email=email).first():
        return {"error": "Email already exists"}, 409
    
    newuser = models.User(
        name=name,
        email=email,
        password_hash=sha256(password.encode()).hexdigest(),
    )

    models.db.session.add(newuser)
    models.db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": newuser.to_dict()
    }), 201