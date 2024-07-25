const btn = document.querySelectorAll("button");

btn.forEach((button) => {
  button.addEventListener("click", function (event) {
    // Prevent the default button behavior (optional)
    event.preventDefault();

    // Get the ID of the button that was clicked
    const clickedbuttonId = button.id;

    if (clickedbuttonId.startsWith("edit_btn")) {
      // Extract the numeric part from the ID
      const btnIndex = clickedbuttonId.split("-")[1];
      
      // Find corresponding save button and form
      const saveBtn = document.getElementById(`save_btn-${btnIndex}`);
      const form = document.getElementById(`form-${btnIndex}`);

      // Toggle display of buttons
      button.style.display = "none";
      saveBtn.style.display = "block";

      // Enable inputs within the form
      const inputs = form.getElementsByTagName("input");
      for (let i = 0; i < inputs.length; i++) {
        inputs[i].removeAttribute("disabled");
      }
    }

    console.log("Clicked button ID:", clickedbuttonId);
  });
});
