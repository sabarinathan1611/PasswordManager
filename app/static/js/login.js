const front = document.querySelector(".front");
const back = document.querySelector(".back");
const card = document.querySelector(".card");
const tologin = document.querySelector(".tologin");
const tosignup = document.querySelector(".tosignup");

tologin.addEventListener("click", () => {
  const front_display = window
    .getComputedStyle(front)
    .getPropertyValue("display");
  const back_display = window
    .getComputedStyle(back)
    .getPropertyValue("display");
  console.log("back_display");
  if (front_display === "block" || back_display === "none") {
    card.classList.add("rotate_card");

    setTimeout(() => {
      front.style.display = "none";
      back.style.display = "flex";
      card.classList.remove("rotate_card");
    }, 500);
  } else if (back_display == "flex") {
    card.classList.add("rotate_card");
    console.log("in back dis");

    setTimeout(() => {
      front.style.display = "flex";
      back.style.display = "none";
      card.classList.remove("rotate_card");
    }, 500);
  }
});

tosignup.addEventListener("click", () => {
  const front_display = window
    .getComputedStyle(front)
    .getPropertyValue("display");
  const back_display = window
    .getComputedStyle(back)
    .getPropertyValue("display");
  console.log("back_display");
  if (front_display === "block" || back_display === "none") {
    card.classList.add("rotate_card");

    setTimeout(() => {
      front.style.display = "none";
      back.style.display = "flex";
      card.classList.remove("rotate_card");
    }, 500);
  } else if (back_display == "flex") {
    card.classList.add("rotate_card");
    console.log("in back dis");

    setTimeout(() => {
      front.style.display = "flex";
      back.style.display = "none";
      card.classList.remove("rotate_card");
    }, 500);
  }
});
