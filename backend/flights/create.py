import datetime
from flask import Blueprint, request, jsonify

import models
import auth
import common

flights_create = Blueprint("flights_create", __name__)

@flights_create.route("/flights/create", methods=["POST"])
@auth.auth.login_required
def createFlight():
    """
    Creates a new flight.
    """
    requestUser = auth.getRequestUser(sessionkey=request.headers.get(common.SESSION_KEY_HEADER_NAME))
    if not requestUser:
        return ({"error": "Invalid session key"}, 401)
    if not requestUser.utype == common.USER_TYPE_ADMIN:
        return ({"error": "Unauthorized"}, 403)
    
    requestdata = request.get_json(force=True)
    if not requestdata:
        return ({"error": "Invalid JSON data"}, 400)
    
    flightno = requestdata.get("flightno")
    airline = requestdata.get("airline")
    source = requestdata.get("source")
    destination = requestdata.get("destination")
    departuretime = requestdata.get("arrivaltime") # Of the form "YYYY-MM-DD HH:MM:SS" (Defined in common.py)
    sourcetime = requestdata.get("departuretime") # Of the form "YYYY-MM-DD HH:MM:SS"
    price = int(requestdata.get("price"))
    seats = int(requestdata.get("seats", 60))
    
    if not flightno or not airline or not source or not destination or not departuretime or not sourcetime or not price or not seats:
        return {"error": "Missing data"}, 400
    if type(flightno) != str or type(airline) != str or type(source) != str or type(destination) != str or type(departuretime) != str or type(sourcetime) != str or type(price) != int or type(seats) != int:
        return {"error": "Invalid data types"}, 400
    
    try:
        departuretime = datetime.datetime.strptime(departuretime, common.DATETIME_PARSE_PATTERN)
        sourcetime = datetime.datetime.strptime(sourcetime, common.DATETIME_PARSE_PATTERN)
    except ValueError:
        return {"error": "Invalid date format"}, 400
    
    if departuretime < datetime.datetime.now() or sourcetime < datetime.datetime.now():
        return {"error": "Invalid date"}, 400
    if price < 0 or seats < 0:
        return {"error": "Invalid price or seats"}, 400
    if sourcetime > departuretime:
        return {"error": "Invalid time"}, 400
    
    flight = models.Flight(
        airline=airline,
        flight_no=flightno,
        departure=source,
        arrival=destination,
        departure_time=sourcetime,
        arrival_time=departuretime,
        price=price,
        capacity=seats,
        seats_left=seats,
    )
    models.db.session.add(flight)
    models.db.session.commit()
    
    return jsonify({
        "message": "Flight created successfully",
        "flight": flight.to_dict(),
    }), 201