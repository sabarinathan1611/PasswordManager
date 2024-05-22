function editPassword(ID) {
   
    fetch("/edit-password", {
      method: "POST",
      body: JSON.stringify({ ID: ID }),
    }).then((_res) => {
      window.location.href = "/showpass";
      
    });
  }