const sidbar = document.querySelector(".sidebar");

function showSidebar() {
  console.log("in");
  sidbar.style.display = "flex";
  try {
    document.querySelector(".card-container").style.zIndex = "-99";
    console.log(document.querySelector(".card-container").style.zIndex);
  } catch (error) {
    console.log("An error occurred: " + error.message);
  }
}

function hideSidebar() {
  console.log("in");
  sidbar.style.display = "none";
  try {
    document.querySelector(".card-container").style.zIndex = "0";
  } catch (error) {
    console.log("An error occurred: " + error.message);
  }
}
