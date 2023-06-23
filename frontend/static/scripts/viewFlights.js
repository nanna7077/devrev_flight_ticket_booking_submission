fetch(API_URL + `/flights/query`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authentication": window.localStorage.getItem('token')
    },
})
.then((response) => response.json())
.then((data) => {
    if (data.error != undefined) {
        alert(data.error);
        return;
    }
    if (data.flights.length == 0) {
        document.getElementById('flights').innerHTML = `<p style='font-size: 1.5rem; margin-top: 5vh;'>No flights found :(</p>`;
        return;
    }

    document.getElementById('flights').innerHTML = '';
    data.flights.forEach((fl) => {
        var t = `
        <div class="column is-4">
            <div class="card">
                <div class="card-content">
                    <div class="content">
                        <p class="title is-4">Flight Information</p>
                        &nbsp;
                        <p class="subtitle" style='font-size: 0.9rem;'>Airline:         <span style='font-size: 1.1rem;'>`+fl.airline+`</span></p>
                        <p class="subtitle" style='font-size: 0.9rem;'>Flight No:       <span style='font-size: 1.1rem;'>`+fl.flight_no+`</span></p>
                        <p class="subtitle" style='font-size: 0.9rem;'>Departure:       <span style='font-size: 1.1rem;'>`+fl.departure+`</span></p>
                        <p class="subtitle" style='font-size: 0.9rem;'>Arrival:         <span style='font-size: 1.1rem;'>`+fl.arrival+`</span></p>
                        <p class="subtitle" style='font-size: 0.9rem;'>Departure Time:  <span style='font-size: 1.1rem;'>`+fl.departure_time+`</span></p>
                        <p class="subtitle" style='font-size: 0.9rem;'>Arrival Time:    <span style='font-size: 1.1rem;'>`+fl.arrival_time+`</span></p>
                        <p class="subtitle" style='font-size: 0.9rem;'>Price:           <span style='font-size: 1.1rem;'>`+fl.price+`</span></p>
                        <p class="subtitle" style='font-size: 0.9rem;'>Capacity:        <span style='font-size: 1.1rem;'>`+fl.capacity+`</span></p>
                        <p class="subtitle" style='font-size: 0.9rem;'>Seats Left:      <span style='font-size: 1.1rem;'>`+fl.seats_left+`</span></p>
                        &nbsp;`;
            if (fl.seats_left > 0) {
                t += `
                    <button style="width: 100%;" class="button is-primary" onclick = 'window.location.href = "/pages/bookFlight.html?flight_id=`+fl.id+`"'>Book Flight</button>
                `;
            }
            if (window.localStorage.getItem('role') == 'admin') {
                t += `<button style="width: 100%;" class="button is-danger" onclick = 'deleteFlight(`+fl.id+`)'>Delete Flight</button>`;
            }
            t += `</div></div></div></div>`;
        document.getElementById('flights').innerHTML += t;
    })
})

function deleteFlight(id) {
    if (! confirm("Are you sure you want to delete this flight? This action cannot be undone.")) {
        return
    }
    fetch(API_URL + `/flights/delete/` + id, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "Authentication": window.localStorage.getItem('token')
        },
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.error != undefined) {
            alert(data.error);
            return;
        }
        window.location.reload();
    })
}