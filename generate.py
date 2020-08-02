import config
from time import time
from glob import glob

localLogger = config.HelperFunctions.getLogger()
localLogger.debug("Loaded imports")

# generateDownContent = True


try:
    from odf import opendocument, text
except ModuleNotFoundError:
    localLogger.error("Please install odfpy. Instructions: https://pypi.org/project/odfpy/")
    raise ModuleNotFoundError("odf module not found.")

try:
    from datauri import DataURI
except ModuleNotFoundError:
    localLogger.error("Please install python-datauri. Instructions: https://pypi.org/project/python-datauri/")
    raise ModuleNotFoundError("DataURI module not found.")


start = time()


class Document:
    documentCounter = 0

    def __init__(self, path, genContent=False):
        self.path = path
        self.doc = None
        self.elements = {}
        self.dHTML = None
        self.generated = False
        self.id = None

        self.title = ""

        if genContent:
            self.gen()

    def gen(self):
        if self.generated:
            return self.dHTML

        internalArticleText = ""

        self.doc = opendocument.load(self.path)

        for element in self.doc.getElementsByType(text.P):
            styleType = element.attributes[('urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'style-name')]
            if styleType == "Title":
                self.title = str(element)
                internalArticleText += str(config.Page.Tags.Hx(2, text=element))
            elif styleType == "P3":
                internalArticleText += str(config.Page.Tags.Hx(5, text=element, attributes={"class": "subtitle"}))
            else:
                internalArticleText += str(config.Page.Tags.Paragraph(text=element))

        Document.documentCounter += 1

        self.id = config.Page.Tags.generateID(self.title + internalArticleText + str(Document.documentCounter))

        article = config.Page.Tags.Article(text=internalArticleText,
                                           attributes={"id": self.id}
                                           )

        localLogger.debug("Generated document number {}".format(Document.documentCounter))

        self.dHTML = str(article)

        self.generated = True

        return self.dHTML


class DocumentCluster:
    def __init__(self, path):
        self.documents = []  # get all the documents

        for document in glob(path + "/*"):
            self.documents.append(Document(document))

        self.sectionName = config.path.basename(path)
        self.id = config.Page.Tags.generateID(self.sectionName + path)

    def collectHTML(self):
        dHTML = ""
        for document in self.documents:
            dHTML += document.gen()

        h1 = config.Page.Tags.Hx(1, text=self.sectionName)
        header = config.Page.Tags.Header(text=h1)

        section = config.Page.Tags.Section(text=header + dHTML, attributes={"id": self.id, "class": "Closed"})

        return str(section)


localLogger.debug("Defined Document Data structures")

# Generate all the file
documentClusters = []

for File in glob(config.Generation.searchPath):
    localLogger.debug("Found file at: {}".format(File))
    documentClusters.append(DocumentCluster(File))

# Add all the sections

bareHTML = config.Page.bareHeader
beefHTML = config.Page.fullHeader
downHTML = config.Page.embedHeader

midHTML = ""

for documentCluster in documentClusters:
    midHTML += documentCluster.collectHTML()

if len(documentClusters) == 0:
    midHTML += str(config.Page.Tags.Hx(1, text="No documents found"))

localLogger.info("There are {} document clusters".format(len(documentClusters)))

localLogger.info("Generating TOC...")

tocHTML = ""

folderFilePairs = dict()

i = 0
for documentCluster in documentClusters:
    i += 1

    innerHTML = str(config.Page.Tags.FigureImageCombo(config.Generation.publicFolderImageLocation,
                                                      "Cluster {}".format(i),
                                                      attributes=
                                                      {"class": "figure Folder",
                                                       "onclick": "OpenFolder(this)",
                                                       "data-openid": str(documentCluster.id)},
                                                      imageAttributes={"class": "figure-img img-fluid"},
                                                      imageSubtextAttributes={"class": "figure-caption text-center"}
                                                      )
                    )

    tocItemsHTML = ""

    tocItemsHTML += str(config.Page.Tags.FigureImageCombo(config.Generation.publicBackImageLocation,
                                                          "Go back",
                                                          attributes=
                                                          {"class": "figure File Back Closed",
                                                           "onclick": "ShowAllFolders()"
                                                           },
                                                          imageAttributes={"class": "figure-img img-fluid"},
                                                          imageSubtextAttributes={"class": "figure-caption text-center"}
                                                          )
                        )

    for documentDC in documentCluster.documents:
        tocItemsHTML += str(config.Page.Tags.FigureImageCombo(config.Generation.publicFileImageLocation,
                                                              documentDC.title,
                                                              attributes={"class": "figure File Closed",
                                                                          "data-openid": str(documentDC.id),
                                                                          "onclick": "OpenSection(this)"
                                                                          },
                                                              imageAttributes={"class": "figure-img img-fluid"},
                                                              imageSubtextAttributes=
                                                              {"class": "figure-caption text-center"}
                                                              )
                            )

    innerHTML += str(config.Page.Tags.Div(text=tocItemsHTML))

    tocHTML += str(config.Page.Tags.Div(text=innerHTML, attributes={"class": "FolderAndFiles"}))

nav = config.Page.Tags.Nav(text=tocHTML, attributes={"class": "container"})
midMain = config.Page.Tags.Main(text=midHTML, attributes={"class": "container"})

minFlexWrapper = config.Page.Tags.Div(text=nav + midMain, attributes={"class": "FlexWrapper"})

pageContainer = config.Page.Tags.Div(text=minFlexWrapper + config.Page.FooterTag, attributes={"class": "pageContainer"})

bareHTML += midHTML + config.Page.HTMLEnd
beefHTML += str(pageContainer) + config.Page.HTMLEnd
downHTML += str(pageContainer) + "{resourcePackVarScript}" + config.Page.HTMLEnd

localLogger.info("Generating the downloadable version of the website")
resourceCache = dict()
pointer = 0
while pointer != len(downHTML):
    nextImgTag = downHTML.find("<img ", pointer)
    if nextImgTag == -1:
        break

    localLogger.debug("Found img tag at: " + str(nextImgTag))

    srcAttributeStart = downHTML.find("src=\"", nextImgTag)

    localLogger.debug("Found src attribute in img at: " + str(srcAttributeStart))

    srcAttributeStart += len("src=\"")
    srcAttributeEnd = downHTML.find("\"", srcAttributeStart)

    localLogger.debug("Found src attribute end at: " + str(srcAttributeEnd))

    localURL = downHTML[srcAttributeStart:srcAttributeEnd]

    localLogger.debug("Full string: '{}'".format(localURL))

    if localURL not in resourceCache:
        localLogger.debug("Downloading and caching resource.")

        resourceCache[localURL] = localURL
    else:
        localLogger.debug("Resource already downloaded, skipping...")

    pointer = downHTML.find(">", nextImgTag + 1)


localLogger.info("Making resources for download and packing them into the resource pack variable")

for resource in resourceCache:
    fileLoc = "Public" + resourceCache[resource]
    makeResource = DataURI.from_file(fileLoc, base64=True).replace("/n", "")
    localLogger.debug("Made URI for '{}' from file in '{}'".format(resourceCache[resource], fileLoc))

resourcePackVarLine = config.HelperFunctions.Read("PublicResources/Scripts/resourcePackVarTemplate.js")
resourcePackVarLine = resourcePackVarLine.replace("{}", str(resourceCache))

resourcePackVarScript = config.Page.Tags.HTMLElement("script", selfClosing=False, innerHTML=resourcePackVarLine)
resourcePackVarScript = str(resourcePackVarScript)

downHTML = downHTML.replace("{resourcePackVarScript}", resourcePackVarScript)

localLogger.info("Finishing building, writing...")

config.HelperFunctions.Save(config.Generation.MinimumPage, bareHTML)
config.HelperFunctions.Save(config.Generation.MainPage, beefHTML)
config.HelperFunctions.Save(config.Generation.DownloadPage, downHTML)

localLogger.info("Data written to '{}' folder".format(config.Generation.buildLocation))
localLogger.info("Took: {}s".format(round(time() - start, 2)))
