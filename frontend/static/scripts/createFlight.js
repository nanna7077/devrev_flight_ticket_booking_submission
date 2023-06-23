document.getElementById('createFlightButton').addEventListener('click', (event) => {
    var flightno = document.getElementById('flightno').value;
    var airline = document.getElementById('airline').value;
    var source = document.getElementById('source').value;
    var destination = document.getElementById('destination').value;
    var departure = document.getElementById('departuretime').value;
    var arrival = document.getElementById('arrivaltime').value;
    var price = document.getElementById('price').value;
    var seats = document.getElementById('seats').value;
    var data = {
        flightno: flightno,
        airline: airline,
        source: source,
        destination: destination,
        arrivaltime: arrival.replace('T', ' '),
        departuretime: departure.replace('T', ' '),
        price: price,
        seats: seats
    };
    
    fetch(API_URL + `/flights/create`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authentication": window.localStorage.getItem('token')
        },
        body: JSON.stringify(data)
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.error != undefined) {
            alert(data.error);
            return;
        }
        alert("Flight created successfully with ID "+data.flight.id+" !");
        window.location.href = '/';
    })
})