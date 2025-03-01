document.addEventListener("DOMContentLoaded", function () {
    console.log("Website Loaded Successfully!");
});

document.addEventListener("DOMContentLoaded", function () {
    let currentLocation = window.location.pathname.split("/").pop();
    let navLinks = document.querySelectorAll("nav ul li a");

    navLinks.forEach(link => {
        if (link.getAttribute("href") === currentLocation) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
});
