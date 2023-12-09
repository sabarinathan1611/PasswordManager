
const features_bar = document.querySelectorAll(".features-bar");
const all_cards = document.querySelectorAll(".card")
features_bar.forEach(bar => {
    bar.addEventListener("click", ()=>{
        let index = bar.getAttribute("index");
        showCard(index);
        features_bar.forEach(feature => {
            feature.classList.remove("done")
            if (feature.classList.contains("active")) {
                feature.classList.add("done");
            }
            feature.classList.remove("active");
        });
        bar.classList.add("active");
    });
});

function showCard(index){

    all_cards.forEach(card => {
        let cardIndex = card.getAttribute("index");
        if (cardIndex == index) {
            card.classList.add("active");
        }else{
            card.classList.remove("active");
        }
    });

}