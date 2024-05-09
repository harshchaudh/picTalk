document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function () {
        var flashMessage = document.getElementById("flash-message");
        flashMessage.classList.add("fade-out");
        setTimeout(function () {
            flashMessage.style.display = "none";
        }, 1000); 
    }, 5000); // Hide the flash message after 5 seconds
});
