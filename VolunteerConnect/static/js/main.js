document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded"); // Debugging

    const userTypeSelect = document.getElementById("id_role");
    const ngoFields = document.getElementById("ngoFields");

    if (userTypeSelect && ngoFields) {
        console.log("Elements found"); // Debugging

        function toggleNgoFields() {
            console.log("Selected role:", userTypeSelect.value); // Debugging
            ngoFields.style.display = userTypeSelect.value.toLowerCase() === "ngo" ? "block" : "none";
        }

        userTypeSelect.addEventListener("change", toggleNgoFields);
        toggleNgoFields(); // Ensure fields show/hide on page load
    } else {
        console.error("User type select or NGO fields not found!");
    }
});
