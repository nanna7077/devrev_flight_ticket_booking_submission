var flightCache = {};

function getAllFlights() {
    fetch(API_URL + '/flights/listall', {
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
            return;
        }
        var baseHTML = '<option default>Select Flight</option>';
        data.flights.forEach((flight) => {
            baseHTML += `
            <option value="`+flight.flight_no+`">`+flight.flight_no+`</option>
            `;
            if (flightCache[flight.flight_no] == undefined) {
                flightCache[flight.flight_no] = [];
            } else {
                flightCache[flight.flight_no].push(flight);
            }
        })
        document.getElementById('flightnumber').innerHTML = baseHTML;
    })
}

document.getElementById('flightnumber').addEventListener('change', (event) => {
    var fID = event.target.value;
    if (flightCache[fID] != undefined) {
        var baseHTML = '<option default>Select Flight</option>';
        flightCache[fID].forEach((booking) => {
            baseHTML += `<option value = '`+booking.depatureTime+`'>`+booking.depatureTime+`</option>`;
        })
        document.getElementById('depaturetime').innerHTML = baseHTML;
        fetch(API_URL + '/tickets/view/flight/' + document.getElementById('flightnumber').value, {
            method: "GET",
            headers: new Headers({
                "Content-Type": "application/json",
                "Authentication": window.localStorage.getItem('token')
            })
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error != undefined) {
                alert(data.error);
                return;
            }
            var baseHTML = `
            <thead>
                <tr>
                <th>Passenger Name</th>
                <th>Verifiable Type</th>
                <th>Verifiable ID</th>
                <th>Seat No</th>
                <th>Status</th>
                </tr>
            </thead>
            <tbody>
            `;
            data.tickets.forEach((ticket) => {
                baseHTML += `
                <tr>
                    <td>`+ticket.passenger_name+`</td>
                    <td>`+ticket.passenger_verifiable_type+`</td>
                    <td>`+ticket.passenger_verifiable_id+`</td>
                    <td>`+ticket.seat_no+`</td>
                    <td>`+ticket.status+`</td>
                </tr>
                `;
            })
            baseHTML += `
            </tbody>
            `;
            document.getElementById('flights').innerHTML = baseHTML;
        })
    }
})

document.getElementById('depaturetime').addEventListener('change', (event) => {
    fetch(API_URL + '/tickets/view/flight/' + document.getElementById('flightnumber').value + '?depatureTime=' + document.getElementById('depaturetime').value, {
        method: "GET",
        headers: new Headers({
            "Content-Type": "application/json",
            "Authentication": window.localStorage.getItem('token')
        })
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.error != undefined) {
            alert(data.error);
            return;
        }
        var baseHTML = `
        <thead>
            <tr>
            <th>Passenger Name</th>
            <th>Verifiable Type</th>
            <th>Verifiable ID</th>
            <th>Seat No</th>
            <th>Status</th>
            </tr>
        </thead>
        <tbody>
        `;
        data.tickets.forEach((ticket) => {
            baseHTML += `
            <tr>
                <td>`+ticket.passenger_name+`</td>
                <td>`+ticket.passenger_verifiable_type+`</td>
                <td>`+ticket.passenger_verifiable_id+`</td>
                <td>`+ticket.seat_no+`</td>
                <td>`+ticket.status+`</td>
            </tr>
            `;
        })
        baseHTML += `
        </tbody>
        `;
        document.getElementById('flights').innerHTML = baseHTML;
    })
})

getAllFlights();