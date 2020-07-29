function decompress() {
    let images = document.getElementsByTagName("img");
    for (let image = 0; image > images.length; image++) {
        let imgURL = images[image].getAttribute("src");
        if (imgURL in contentReplacePairs) {
            images[image].setAttribute("src", contentReplacePairs[imgURL])
        }
    }

    console.log("Decompression finished.");
}