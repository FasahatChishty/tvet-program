const form = document.getElementById("registerForm");

if (form) {
    form.addEventListener("submit", function (e) {
        const roll = document.getElementById("roll").value;
        const password = document.getElementById("password").value;
        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();

        // Name validation
        if (name.length < 2) {
            e.preventDefault();
            alert("Name must be at least 2 characters long");
            return;
        }

        // Roll format
        const rollPattern = /^\d{4}[A-Z]-[A-Z]{3}-\d{3}$/;
        if (!rollPattern.test(roll)) {
            e.preventDefault();
            alert("Roll number must be like 2022F-BSE-250");
            return;
        }

        // Email
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            e.preventDefault();
            alert("Enter valid email");
            return;
        }

        // Password
        if (password.length < 6) {
            e.preventDefault();
            alert("Password must be at least 6 characters");
            return;
        }

        // Disable button (no double submit)
        const btn = document.getElementById("registerBtn");
        if (btn) {
            btn.disabled = true;
            btn.textContent = "Registering...";
        }
    });
}

// Modal safe function
window.closeModal = function () {
    const modal = document.getElementById("modal");
    if (modal) modal.style.display = "none";
};