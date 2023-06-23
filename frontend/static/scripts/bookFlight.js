var flightID = new URLSearchParams(window.location.href.split('?')[1]).get('flight_id');

if (flightID == null || flightID == undefined) {
    alert("No flightID provided");
    window.location.href = "/pages/viewFlights.html";
}

fetch(API_URL + `/flights/individual/${flightID}`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authentication": window.localStorage.getItem('token')
    }
})
.then((response) => response.json())
.then((data) => {
    if (data.error != undefined) {
        alert(data.error);
        window.location.href = "/pages/viewFlights.html";
    }
    Object.entries(data.flight).forEach((entry) => {
        document.getElementById('flightdetails').innerHTML += `<div><b>${entry[0]}</b>: ${entry[1]}</div>`;
    })
})

document.getElementById('bookFlightButton').addEventListener('click', () => {
    fetch(API_URL + `/tickets/create`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authentication": window.localStorage.getItem('token')
        },
        body: JSON.stringify({
            flightID: flightID,
            passenger_name: document.getElementById('passengerName').value,
            passenger_verifiable_type: document.getElementById('passengerVerificationType').value,
            passenger_verifiable_id: document.getElementById('passengerVerificationNumber').value,
            seat_no: document.getElementById('seatNumber').value
        })
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.error != undefined) {
            alert(data.error);
            return;
        }
        alert("Flight booked!");
        window.location.href = "/pages/viewBookings.html";
    })
})