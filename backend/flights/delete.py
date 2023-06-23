import datetime
from flask import Blueprint, request, jsonify

import models
import auth
import common

flights_delete = Blueprint("flights_delete", __name__)

@flights_delete.route("/flights/delete/<int:ID>", methods=["DELETE"])
@auth.auth.login_required
def deleteFlight(ID):
    """
    Deletes a flight based on the given parameters.
    Supports multiple parameters to be queried for at the same time.
    """
    requestUser = auth.getRequestUser(sessionkey=request.headers.get(common.SESSION_KEY_HEADER_NAME))
    if not requestUser:
        return ({"error": "Invalid session key"}, 401)
    if requestUser.utype != 1:
        return ({"error": "Unauthorized"}, 403)
    
    flight = models.Flight.query.filter_by(id=ID).first()
    if not flight:
        return ({"error": "Flight not found"}, 404)
    
    tickets = models.Ticket.query.filter_by(flight_id=ID).all()
    """
    Removing tickets for the set flight.
    """

    for ticket in tickets:
        models.db.session.delete(ticket)
    
    models.db.session.delete(flight)
    models.db.session.commit()

    return jsonify({
        "message": "Flight deleted"
    }), 200