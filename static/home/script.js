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
    async function hashPasswordAndSubmit(event, formType) {
        event.preventDefault(); // Prevent default form submission
    
        if (formType === "login") {
            const passwordField = document.getElementById("password");
            const password = passwordField.value;
    
            if (!password) {
                console.error("Password field is empty!");
                return;
            }
    
            const hashedPassword = await sha256(password);
            console.log("Login Hashed Password:", hashedPassword);
            
            passwordField.value = hashedPassword;
        } 
        else if (formType === "register") {
            const passwordField = document.getElementById("registerPassword");
            const password = passwordField.value;
    
            if (!password) {
                console.error("Register password field is empty!");
                return;
            }
    
            const hashedPassword = await sha256(password);
            console.log("Register Hashed Password:", hashedPassword);
            
            passwordField.value = hashedPassword;
        }
    
        event.target.submit(); // Now submit the form
    }
    
    // Attach event listeners separately for login and register forms
    document.querySelector('.loginForm form').onsubmit = (event) => hashPasswordAndSubmit(event, "login");
    document.querySelector('.registerForm form').onsubmit = (event) => hashPasswordAndSubmit(event, "register");
    

    // SHA-256 hashing function
    async function sha256(message) {
        const msgBuffer = new TextEncoder().encode(message);
        const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(byte => byte.toString(16).padStart(2, "0")).join("");
    }
});