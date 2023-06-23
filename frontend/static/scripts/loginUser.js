document.getElementById("loginUserButton").addEventListener("click", () => {
    fetch(API_URL + `/users/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
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
        window.localStorage.setItem("token", data.sessionkey);
        if (data.user.utype == 1) {
            window.localStorage.setItem("role", "admin");
        }
        window.location.href = "/index.html";
      });
});  