document.addEventListener("DOMContentLoaded", function () {
    feather.replace(); // Enables Feather icons

    const userTypeSelect = document.getElementById("id_user_type");
    const ngoFields = document.getElementById("ngoFields");

    if (userTypeSelect) { // Ensure element exists to avoid errors
        function toggleNgoFields() {
            ngoFields.style.display = userTypeSelect.value === "ngo" ? "block" : "none";
        }

        userTypeSelect.addEventListener("change", toggleNgoFields);
        toggleNgoFields(); // Run on page load
    }
});
