const API_URL = "http://localhost:5000"

// NavBar Component

document.getElementById('navbar').innerHTML = `
<div class="navbar-brand">
    <a class="navbar-item" href="/">
        <div class="title is-5">Flight Booking System</div>
    </a>

    <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false"
        data-target="navbarBasic">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
    </a>
</div>

<div id="navbarBasic" class="navbar-menu">
    <div class="navbar-end">
        <div class="navbar-item" id = "buttonareanav">
            
            
        </div>
    </div>
</div>
`;

if (! window.localStorage.getItem('token')) {
    document.getElementById('buttonareanav').innerHTML = `
    <div class="buttons" id = "loginbuttons">
        <a class="button is-primary" onclick = 'window.location.href = "/pages/registerUser.html";'>
            <strong>Sign up</strong>
        </a>
        <a class="button is-light" onclick = 'window.location.href = "/pages/loginUser.html";'>
            Log in
        </a>
    </div>
    `;
} else {
    fetch(API_URL + `/users/me`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authentication": window.localStorage.getItem('token')
        }
    })
    .then((response) => response.json())
    .then((data) => {
        var baseHTML = `
        <div class="buttons" id = "navactions">
            <a class="button is-primary" onclick = 'window.location.href = "/pages/viewFlights.html";'>
                Search Flights
            </a>
            <a class="button is-light">
                My Bookings
            </a>
            `;
        if (data.error != undefined) {
            alert(data.error);
            return;
        }
        if (data.user.utype == 1) {
            baseHTML += `
            <a class="button is-light" onclick = 'window.location.href = "/pages/createFlight.html";'>
                Create Flight
            </a>
            <a class="button is-light" onclick = 'window.location.href = "/pages/viewFlights.html";'>
                Delete Flight
            </a>
            <a class="button is-light" onclick = 'window.location.href = "/pages/viewBookings.html";'>
                View Bookings
            </a>
            `;
        }
        baseHTML += `<a class="button is-light" onclick = "window.localStorage.clear();window.location.href='/';">
                Log out
            </a>
            <div class="navbar-item" style="justify-items: center; align-content: center;">
                Logged In as&nbsp;<b>`+data.user.name+`</b>
            </div>
        </div>`;
        document.getElementById('buttonareanav').innerHTML = baseHTML;
    });
    // Add create/delete flight button if user is admin
    // Add View bookings based on flight number and time if user is admin
}