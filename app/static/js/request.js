function editPassword(ID) {
    fetch("/edit-password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ ID: ID })
    }).then((_res) => {
        if (_res.ok) {
            window.location.href = "/showpass";
        } else {
            // Handle error
            alert("Error updating password");
        }
    });
}
