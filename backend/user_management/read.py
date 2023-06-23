from hashlib import sha256
import re
from flask import Blueprint, request, jsonify

import models
import auth
import common

user_management_read = Blueprint("user_management_read", __name__)

@user_management_read.route("/users/login", methods=["POST"])
def login():
    """
    Logs in a user.
    """
    
    requestdata = request.get_json(force=True)
    if not requestdata:
        return ({"error": "Invalid JSON data"}, 400)
    
    email = requestdata.get("email")
    password = str(requestdata.get("password"))

    if not email or not password:
        return {"error": "Missing data"}, 400
    if not re.match(common.EMAIL_VALIDATION_PATTERN, email):
        return {"error": "Invalid email"}, 400
    
    user = models.User.query.filter_by(email=email).first()
    if not user:
        return {"error": "Invalid email or password"}, 401
    if user.password_hash != sha256(password.encode()).hexdigest():
        return {"error": "Invalid email or password"}, 401
    
    sessionkey = auth.generateSessionKey(user.id)
    
    return jsonify({
        "message": "User logged in successfully",
        "user": user.to_dict(),
        "sessionkey": sessionkey,
    }), 200

@user_management_read.route("/users/<int:userid>", methods=["GET"])
@auth.auth.login_required
def getUser(userid):
    """
    Returns the user object of the user with the specified userid.
    """
    requestUser = auth.getRequestUser(sessionkey=request.headers.get(common.SESSION_KEY_HEADER_NAME))
    if not requestUser:
        return ({"error": "Invalid session key"}, 401)
    if not (requestUser.utype == common.USER_TYPE_ADMIN or requestUser.id == userid):
        return ({"error": "Unauthorized"}, 403)
    
    user = models.User.query.filter_by(id=userid).first()
    if not user:
        return ({"error": "User not found"}, 404)
    
    return jsonify({
        "message": "User found",
        "user": user.to_dict(),
    }), 200

@user_management_read.route("/users/me", methods=["GET"])
@auth.auth.login_required
def getMe():
    """
    Returns the user object of the user making the request.
    """
    requestUser = auth.getRequestUser(sessionkey=request.headers.get(common.SESSION_KEY_HEADER_NAME))
    if not requestUser:
        return ({"error": "Invalid session key"}, 401)
    
    return jsonify({
        "message": "User found",
        "user": requestUser.to_dict(),
    }), 200
