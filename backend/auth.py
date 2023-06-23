import random
import string

from flask_httpauth import HTTPTokenAuth

from models import *

"""
We are using Flask-HTTPAuth for authentication, specifically the HTTP Token Authentication method.
Using a token-based authentication is easier to implement and is more secure than using a session-based authentication.
"""

auth = HTTPTokenAuth(scheme="Bearer", realm=None, header="Authentication")


@auth.verify_token
def verify_password(sessionkey):
    """
    This function is called by Flask-HTTPAuth to verify the sessionkey.
    It returns True if the sessionkey is valid, and False otherwise.

    This is the function that is called by the @auth.login_required decorator. It is not called directly, but can also be called directly if needed.
    """

    return Session.query.filter_by(sessionkey=sessionkey).first() != None


@auth.error_handler
def handle401(error):
    """
    This function is called when the user is not authenticated.
    It is used to return a JSON response instead of the default HTML response.
    """
    
    return {"error": "UnAuthorized"}, 401


# Functions to help with authentication. These helps in reducing code duplication.

def getRequestUser(sessionkey):
    """
    Returns the user object of the user who made the request based on the sessionkey. 
    This allows for better security as the user object is fetched from the database instead of being stored and reused from client-side.
    """

    requestsession = Session.query.filter_by(sessionkey=sessionkey).first()
    if not requestsession:
        return ({"error": "Invalid SessionKey"}, 404)
    
    requestuser = User.query.filter_by(id=requestsession.userid).first()
    if not requestuser:
        return ({"error": "Invalid SessionKey"}, 404)
    
    return requestuser

def generateSessionKey(user):
    """
    Generates a sessionkey for the user and stores it in the database.
    """

    sessionkey = "".join([random.choice(string.ascii_letters) for _ in range(20)])
    newsession = Session(
        sessionkey=sessionkey,
        userid=user
    )
    
    db.session.add(newsession)
    db.session.commit()
    
    return sessionkey