import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    utype = db.Column(db.Integer, nullable=False, default = 0) # 0 for regular user, 1 for admin

    def __repr__(self):
        """Return a string representation of the user."""
        return f"<User {self.name} ({self.id})>"
    
    def to_dict(self):
        """Return a dictionary representation of the user. Useful for JSONifying."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "utype": self.utype
        }

class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    sessionkey = db.Column(db.String, nullable=False)
    started_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    is_expired = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        """Return a string representation of the session."""
        return f"<Session {self.id} ({self.userid})>"
    
    def to_dict(self):
        """Return a dictionary representation of the session. Useful for JSONifying."""
        return {
            "id": self.id,
            "userid": self.userid,
            "sessionkey": self.sessionkey,
            "started_on": self.started_on,
            "is_expired": self.is_expired
        }

class Flight(db.Model):
    """
    We are going with the assumption that all flights are one-way as it is easier to implement.
    Return flights can be trivially implemented by adding another flight with the same details but with the departure and arrival swapped.
    We are also going with the assumption that all flights are direct flights, i.e. no layovers. Layovers can be implemented in the future by adding another flight with the same details but with the departure time and arrival time changed.
    """

    __tablename__ = "flights"

    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String, nullable=False)
    flight_no = db.Column(db.String, nullable=False)
    departure = db.Column(db.String, nullable=False)
    arrival = db.Column(db.String, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default = 60)
    seats_left = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Return a string representation of the flight."""
        return f"<Flight {self.airline} {self.flight_no} ({self.id})>"
    
    def to_dict(self):
        """Return a dictionary representation of the flight. Useful for JSONifying."""
        return {
            "id": self.id,
            "airline": self.airline,
            "flight_no": self.flight_no,
            "departure": self.departure,
            "arrival": self.arrival,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "price": self.price,
            "capacity": self.capacity,
            "seats_left": self.seats_left,
        }
    
class Ticket(db.Model):
    """
    Each booking is represented by a ticket.
    The seats are represented by a string of the seat number, e.g. "A1", "B2", etc. This is easier to implement than a 2D array.
    """

    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    passenger_name = db.Column(db.String, nullable=False) # name of passenger as the booking system does not require the passenger to be the user
    passenger_verifiable_type = db.Column(db.String, nullable=False)
    passenger_verifiable_id = db.Column(db.String, nullable=False) # e.g. passport number, IC number, etc.
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)
    seat_no = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False, default = 0) # 0 for booked, 1 for cancelled

    def __repr__(self):
        """Return a string representation of the ticket."""
        return f"<Ticket {self.id} ({self.user_id})>"
    
    def to_dict(self):
        """Return a dictionary representation of the ticket. Useful for JSONifying."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "passenger_name": self.passenger_name,
            "passenger_verifiable_type": self.passenger_verifiable_type,
            "passenger_verifiable_id": self.passenger_verifiable_id,
            "flight_id": self.flight_id,
            "seat_no": self.seat_no,
            "status": self.status
        }

