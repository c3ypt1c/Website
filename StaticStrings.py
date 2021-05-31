class Logging:
    loggerFolder = "logs/"
    loggerPathTemplate = "runtime.{}.log"


class Generation:
    searchPath = "Sections/*"
    buildNumberLocation = "build number"

    publicFolderImageLocation = "Resources/PageImages/folder-sharp.svg"
    publicFolderOpenImageLocation = "Resources/PageImages/folder-open-sharp.svg"
    publicFileImageLocation = "Resources/PageImages/document-text-sharp.svg"
    publicBackImageLocation = "Resources/PageImages/arrow-back-sharp.svg"

    buildLocation = "/srv/http/WebsitePublic/"

    MainPage = buildLocation + "chicken.html"
    MinimumPage = buildLocation + "bare.html"
    DownloadPage = buildLocation + "down.html"
