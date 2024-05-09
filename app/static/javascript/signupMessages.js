document.getElementById("signup-username").addEventListener("input", function() {
    var usernameInput = document.getElementById("signup-username");
    var messageElement = document.getElementById("message");
    if (usernameInput.value.length < 6) {
        messageElement.innerHTML = "Username must be at least 6 characters long.";
    } else {
        messageElement.innerHTML = ""; // Clear the message if username is valid
    }
});

document.getElementById("signup-psw").addEventListener("input", function() {
    var passwordInput = document.getElementById("signup-psw");
    var messageElement = document.getElementById("message");
    if (passwordInput.value.length < 8) {
        messageElement.innerHTML = "Password must be at least 8 characters long.";
    } else {
        messageElement.innerHTML = ""; // Clear the message if password is valid
    }
});