import datetime
from flask import Blueprint, request, jsonify

import models
import auth
import common

tickets_read = Blueprint("tickets_read", __name__)

@tickets_read.route("/tickets/view/<int:ticketID>", methods=["GET"])
@auth.auth.login_required
def viewTicket(ticketID):
    """
    Views a ticket.
    """
    requestUser = auth.getRequestUser(sessionkey=request.headers.get(common.SESSION_KEY_HEADER_NAME))
    if not requestUser:
        return ({"error": "Invalid session key"}, 401)

    ticket = models.Ticket.query.filter_by(id=ticketID).first()
    if not ticket:
        return {"error": "Invalid ticket ID"}, 404

    return jsonify({
        "message": "Ticket found",
        "ticket": ticket.to_dict(),
    }
    ), 200

@tickets_read.route("/tickets/view", methods=["GET"])
@auth.auth.login_required
def viewTickets():
    """
    Views all tickets.
    """
    requestUser = auth.getRequestUser(sessionkey=request.headers.get(common.SESSION_KEY_HEADER_NAME))
    if not requestUser:
        return ({"error": "Invalid session key"}, 401)
    
    userID = requestUser.id
    if requestUser.utype == common.USER_TYPE_ADMIN:
        if request.args.get("userID") and models.User.query.filter_by(id=request.args.get("userID")).first() is not None:
            userID = request.args.get("userID")

    tickets = models.Ticket.query.filter_by(user_id=userID).all()
    if not tickets:
        return {"error": "No tickets found"}, 404

    return jsonify({
        "message": "Tickets found",
        "tickets": [ticket.to_dict() for ticket in tickets],
    }
    ), 200

@tickets_read.route("/tickets/view/flight/<int:flightID>", methods=["GET"])
def viewTicketsByFlight(flightID):
    """
    Views all tickets for a flight.
    """
    requestUser = auth.getRequestUser(sessionkey=request.headers.get(common.SESSION_KEY_HEADER_NAME))
    if not requestUser:
        return ({"error": "Invalid session key"}, 401)
    
    try:
        departureTime = datetime.datetime.fromtimestamp(int(request.args.get("departureTime")))
    except:
        departureTime = None

    # tickets = models.Ticket.query.filter(
    #     models.Flight.flight_no == flightID
    # ).filter(
    #     departureTime != None and models.Flight.departureTime == departureTime
    # ).filter(
    #     models.Ticket.flight_id == models.Flight.flight_no
    # ).all()
    tickets = models.Ticket.query.filter_by().all()
    if not tickets:
        return {"error": "No tickets found"}, 404

    return jsonify({
        "message": "Tickets found",
        "tickets": [ticket.to_dict() for ticket in tickets],
    }
    ), 200
