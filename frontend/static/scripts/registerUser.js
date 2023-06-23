document.getElementById("registerUserButton").addEventListener("click", () => {
    if (document.getElementById("password").value != document.getElementById("confirmPassword").value) {
        alert("Passwords do not match");
        return;
    }
    fetch(API_URL + `/users/register`, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
        if (data.error != undefined) {
            alert(data.error);
            return;
        }
        window.location.href = "/pages/loginUser.html";
        });
});
