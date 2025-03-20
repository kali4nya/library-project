document.addEventListener("DOMContentLoaded", function () {
    // Get the error banner div
    let banner = document.getElementById("error-banner");

    // Read the error message from the data attribute
    let errorMessage = banner.getAttribute("data-error");

    // If an error exists, show the banner with the error message
    if (errorMessage && errorMessage.trim() !== "") {
        banner.textContent = errorMessage;
        banner.style.display = "block";
    } else {
        banner.style.display = "none"; // Ensure it stays hidden if no error
    }

    // Handle form submission
    const form = document.querySelector('form');
    form.onsubmit = async function (event) {
        event.preventDefault(); // Prevent normal form submission

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // Hash the password using SHA-256
        const hashedPassword = await sha256(password);

        // Replace the password field with the hashed password
        document.getElementById("password").value = hashedPassword;

        // Now submit the form with hashed password
        form.submit();
    };

    // SHA-256 hashing function
    async function sha256(message) {
        const msgBuffer = new TextEncoder().encode(message);
        const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(byte => byte.toString(16).padStart(2, "0")).join("");
    }
});