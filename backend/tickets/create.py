import datetime
from flask import Blueprint, request, jsonify

import models
import auth
import common

tickets_create = Blueprint("tickets_create", __name__)

@tickets_create.route("/tickets/create", methods=["POST"])
@auth.auth.login_required
def createTicket():
    """
    Creates a new ticket.
    """
    requestUser = auth.getRequestUser(sessionkey=request.headers.get(common.SESSION_KEY_HEADER_NAME))
    if not requestUser:
        return ({"error": "Invalid session key"}, 401)
    
    requestdata = request.get_json(force=True)
    if not requestdata:
        return ({"error": "Invalid JSON data"}, 400)
    
    flightID = requestdata.get("flightID")
    seat_no = requestdata.get("seat_no")
    passenger_name = requestdata.get("passenger_name")
    passenger_verifiable_type = requestdata.get("passenger_verifiable_type")
    passenger_verifiable_id = requestdata.get("passenger_verifiable_id")

    if not flightID or not seat_no or not passenger_name or not passenger_verifiable_type or not passenger_verifiable_id:
        return {"error": "Missing data"}, 400
    
    flight = models.Flight.query.filter_by(id=flightID).first()
    if not flight:
        return {"error": "Invalid flight ID"}, 404
    if flight.seats_left <= 0:
        return {"error": "No seats left"}, 400
    # if flight.departure_time >= datetime.datetime.utcnow():
    #     return {"error": "Flight has already departed!"}, 400
    # if datetime.timedelta(hours=common.LIMIT_TICKET_BOOKING_BEFORE_DEPARTURE_HOURS) >= (flight.departure_time - datetime.datetime.utcnow()):
    #     return {"error": "Flight is departing in less than an hour! Cannot Book"}, 400
    
    ticket = models.Ticket(
        flight_id=flightID,
        user_id=requestUser.id,
        passenger_name=passenger_name,
        passenger_verifiable_type=passenger_verifiable_type,
        passenger_verifiable_id=passenger_verifiable_id,
        seat_no=seat_no,
    )

    flight.seats_left -= 1
    models.db.session.add(ticket)
    models.db.session.commit()

    return jsonify({
        "message": "Ticket created successfully",
        "ticket": ticket.to_dict(),
    }
    ), 201