import datetime
from flask import Blueprint, request, jsonify

import models
import auth
import common

flights_read = Blueprint("flights_read", __name__)

@flights_read.route("/flights/listall", methods=["GET"])
def listAllFlights():
    """
    Lists all flights.
    """
    flights = models.Flight.query.all()
    if not flights:
        return {"error": "No flights found"}, 404
    
    return jsonify({
        "message": "Flights found",
        "flights": [flight.to_dict() for flight in flights],
    }
    ), 200

@flights_read.route("/flights/query", methods=["GET"])
@auth.auth.login_required
def queryFlights():
    """
    Queries flights based on the given parameters.
    Supports multiple parameters to be queried for at the same time.
    """
    requestUser = auth.getRequestUser(sessionkey=request.headers.get(common.SESSION_KEY_HEADER_NAME))
    if not requestUser:
        return ({"error": "Invalid session key"}, 401)
    
    requestdata = request.args
    
    airline = requestdata.get("airline")
    flightno = requestdata.get("flightno")
    arrival = requestdata.get("source")
    destination = requestdata.get("destination") # Of the form "YYYY-MM-DD HH:MM:SS" (Defined in common.py)
    arrivaltime = requestdata.get("arrivaltime") # Of the form "YYYY-MM-DD HH:MM:SS"
    departuretime = requestdata.get("departuretime")
    price = requestdata.get("price")
    seats = requestdata.get("seats")
    
    try:
        departuretime = datetime.datetime.strptime(departuretime, common.DATETIME_PARSE_PATTERN)
    except:
        departuretime = None
    try:
        arrivaltime = datetime.datetime.strptime(arrivaltime, common.DATETIME_PARSE_PATTERN)
    except:
        arrivaltime = None
    
    flights = models.Flight.query.filter(
        airline != None and models.Flight.airline == airline
    ).filter(
        flightno != None and models.Flight.flightno == flightno
    ).filter(
        arrival != None and models.Flight.arrival == arrival
    ).filter(
        destination != None and models.Flight.destination == destination
    ).filter(
        departuretime != None and models.Flight.departuretime == departuretime
    ).filter(
        arrivaltime != None and models.Flight.arrivaltime == arrivaltime
    ).filter(
        price != None and models.Flight.price == price
    ).filter(
        seats != None and models.Flight.seats == seats
    ).all()

    if not flights:
        return jsonify({
            "message": "No flights found",
            "flights": [flight.to_dict() for flight in models.Flight.query.all()],
        }), 200
    
    return jsonify({
        "message": "Flights found",
        "flights": [flight.to_dict() for flight in flights],
    }), 200

@flights_read.route("/flights/individual/<int:flightID>", methods=["GET"])
@auth.auth.login_required
def getFlight(flightID):
    """
    Gets a flight based on the given flight id.
    """
    requestUser = auth.getRequestUser(sessionkey=request.headers.get(common.SESSION_KEY_HEADER_NAME))
    if not requestUser:
        return ({"error": "Invalid session key"}, 401)
    
    flight = models.Flight.query.filter_by(id=flightID).first()
    if not flight:
        return {"error": "Flight not found"}, 404
    
    return jsonify({
        "message": "Flight found",
        "flight": flight.to_dict(),
    }), 200