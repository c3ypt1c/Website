function decompress() {
    console.log("resourcePack.js: Decompressing...");
    let images = document.getElementsByTagName("img");
    for (let image = 0; image < images.length; image++) {
        let imgURL = images[image].getAttribute("src");
        if (imgURL in contentReplacePairs) {
            console.log("resourcePack.js: Replacing: " + imgURL);
            images[image].setAttribute("src", contentReplacePairs[imgURL]);
        } else {
            console.log("resourcePack.js: Could not replace: " +imgURL);
        }
    }

    console.log("resourcePack.js: Decompression finished.");
}