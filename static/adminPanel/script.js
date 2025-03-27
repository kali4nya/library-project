//password hashing with sha256
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("userForm").addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission !important

        let passwordInput = document.getElementById("password");
        let hashedPasswordInput = document.getElementById("hashedPassword");

        // Hash password with sha256
        const hashBuffer = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(passwordInput.value));
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

        hashedPasswordInput.value = hashHex;
        passwordInput.value = ""; // Important to avoid leaks

        this.submit();
    });
});
