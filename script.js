// Typing Effect
var typed = new Typed(".typing", {
    strings: ["John Doe", "a Web Developer", "an AI Engineer"],
    typeSpeed: 100,
    backSpeed: 50,
    loop: true
});

// Dark Mode Toggle
const toggleButton = document.getElementById("theme-toggle");
toggleButton.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
});
