function validateForm() {
    var fullName = document.getElementById("FullName").value;
    var email = document.getElementById("Email").value;
    var password = document.getElementById("Password").value;
    var confirmPassword = document.getElementById("ConfirmPassword").value;

    if (fullName === "" || email === "" || password === "" || confirmPassword === "") {
        alert("All fields must be filled out");
        return false;
    }

    // Advanced validation for Full Name (minimum 6 characters)
    if (fullName.length < 6) {
        alert("Full Name must be at least 6 characters");
        return false;
    }

    // Advanced validation for Email (using a simple regex for demonstration)
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert("Invalid email format");
        return false;
    }

    // Advanced validation for Password (minimum 8 characters, at least one uppercase, one lowercase, one number, and one special character)
    var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$/;

    if (!passwordRegex.test(password)) {
        alert("Invalid password format. It must be at least 8 characters, contain one uppercase letter, one lowercase letter, one number, and one special character.");
        return false;
    }

    // Check if the password and confirm password match
    if (password !== confirmPassword) {
        alert("Password and Confirm Password do not match");
        return false;
    }

    return true;
}