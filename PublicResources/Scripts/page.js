// For compressed pages
function onLoadCompressed() {
    decompress();
    onLoad();
}

// Normal Onload
function onLoad() {
    console.log("running post-load");
    GoToWelcome();

    MakeGoUp()
    document.addEventListener('scroll', GoUpHandler);
}

let goUpContainer;
function MakeGoUp() {
    // Make container
    goUpContainer = document.createElement("div");
    goUpContainer.id = "returnToTopContainer";

    // Make goUp
    let goUp = document.createElement("div");
    goUp.id = "returnToTop";

    // Assign touch
    goUpContainer.addEventListener("click", GoUpThePage);

    // Add to DOM
    goUpContainer.append(goUp);
    document.body.append(goUpContainer);
}

function GoUpHandler() {
    if(window.scrollY > 0) goUpContainer.classList.add("show");
    else goUpContainer.classList.remove("show");
}

function GoUpThePage() {
    document.documentElement.scrollTop = document.body.scrollTop = 0;
}

console.log("page.js loaded");