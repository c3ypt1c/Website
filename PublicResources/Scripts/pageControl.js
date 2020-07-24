function HideAllFolders() {
    let folders = document.getElementsByClassName("Folder");
    for (let folder = 0; folder < folders.length; folder++) {
        folders[folder].classList.add("Closed");
    }
}

function HideAllFiles() {
    let items = document.getElementsByClassName("File");
    for(let item = 0; item < items.length; item++) {
        items[item].classList.add("Closed");
    }
}

function OpenFolder(id) {
    if(id.classList.contains("Closed")) {
        console.log("Damn, you're fast.")
    }
    else {
        HideAllFolders();
        let items = id.parentNode.getElementsByTagName("figure");

        for (let item = 0; item < items.length; item++) {
            items[item].classList.remove("Closed");
        }

        id.classList.add("Closed");
    }
}

function ShowAllFolders() {
    HideAllFiles();
    let folders = document.getElementsByClassName("Folder");
    for (let folder = 0; folder < folders.length; folder++) {
        folders[folder].classList.remove("Closed");
    }
}

function OpenSection(id) {

}

function JumpToArticle(id) {


}

console.log("pageControl.js loaded");