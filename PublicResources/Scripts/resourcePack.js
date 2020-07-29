function decompress() {
    const contentReplacePairs = {};

    for (let image in document.getElementsByTagName("img")) {
        let imgURL = image.getAttribute("src");
        if (imgURL in contentReplacePairs) {
            image.setAttribute("src", contentReplacePairs[imgURL])
        }
    }

    console.log("Decompression finished.");
}