class Logging:
    loggerFolder = "logs/"
    loggerPathTemplate = "runtime.{}.log"


class Generation:
    searchPath = "Sections/*"
    buildNumberLocation = "build number"

    publicFolderImageLocation = "Resources/PageImages/Folder2.png"
    publicFolderOpenImageLocation = "Resources/PageImages/Folder2open.png"
    publicFileImageLocation = "Resources/PageImages/File2.png"
    publicBackImageLocation = "Resources/PageImages/FileUp2shade3.png"

    buildLocation = "/srv/http/WebsitePublic/"

    MainPage = buildLocation + "chicken.html"
    MinimumPage = buildLocation + "bare.html"
    DownloadPage = buildLocation + "down.html"
