document.addEventListener("DOMContentLoaded", function () {
    console.log("Website Loaded Successfully!");
});

document.addEventListener("DOMContentLoaded", function() {
    document.body.style.opacity = "1"; // Ensure full opacity after loading
});


function toggleCitySelection() {
    var jobLocation = document.getElementById("job_location").value;
    var citySelection = document.getElementById("city-selection");

    if (jobLocation === "Onsite" || jobLocation === "Hybrid") {
        citySelection.style.display = "block";
    } else {
        citySelection.style.display = "none";
    }
}


