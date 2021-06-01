#!/usr/bin/python
from time import time

start = time()

import BodyGenerator
import html_validate
import Errors
from os import remove as removeFile
from glob import glob

localLogger = BodyGenerator.HelperFunctions.getLogger()

generateDownContent = True

try:
    from odf import opendocument, text
except ModuleNotFoundError:
    localLogger.error("Please install odfpy. Instructions: https://pypi.org/project/odfpy/")
    raise ModuleNotFoundError("odf module not found.")

try:
    from datauri import DataURI
except ModuleNotFoundError:
    generateDownContent = False
    localLogger.warning("Content for download will not be generated.")
    localLogger.warning("Please install python-datauri. Instructions: https://pypi.org/project/python-datauri/")

localLogger.debug("Loaded imports")


class Article:
    documentCounter = 0

    def __init__(self, path, genContent=False):
        self.path = path
        self.dHTML = None
        self.generated = False
        self.id = None

        self.title = ""

        if genContent:
            self.gen()

    def genODT(self):
        doc = opendocument.load(self.path)

        internalArticleText = ""

        # Discover and set elements
        for element in doc.getElementsByType(text.P):
            styleType = element.attributes[('urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'style-name')]
            localLogger.debug(styleType + " for " + str(element))
            if str(element).strip() == "":
                localLogger.debug("Skipping empty string")
                continue

            if styleType == "Title":
                self.title = str(element)
                internalArticleText += str(BodyGenerator.Page.Tags.Hx(2, text=element))
            elif styleType == "P3" or styleType == "Subtitle":
                internalArticleText += str(BodyGenerator.Page.Tags.Hx(5, text=element, attributes={"class": "subtitle"}))
            else:
                internalArticleText += str(BodyGenerator.Page.Tags.Paragraph(text=element))

        articleId = BodyGenerator.Page.Tags.generateID(self.title + internalArticleText + str(Article.documentCounter))

        article = BodyGenerator.Page.Tags.Article(text=internalArticleText,
                                                  attributes={"id": articleId}
                                                  )

        return (str(article), articleId)

    def genTXT(self):
        with open(self.path) as f:
            fileData = f.read()

        fileData = [x.strip() for x in fileData.splitlines()]

        if len(fileData) < 2:
            raise Errors.FileTooShort("The file at '{}' has less than 2 lines".format(self.path))

        self.title = fileData[0]
        internalArticleText = BodyGenerator.Page.Tags.Hx(2, self.title)

        for line in fileData[1:]:
            internalArticleText += str(BodyGenerator.Page.Tags.Paragraph(text=line))

        articleId = BodyGenerator.Page.Tags.generateID(self.title + internalArticleText + str(Article.documentCounter))
        article = BodyGenerator.Page.Tags.Article(text=internalArticleText,
                                                  attributes={"id": articleId}
                                                  )

        return (str(article), articleId)

    def gen(self):
        if self.generated:
            return self.dHTML

        if len(self.path) < len(".xyz"):
            raise Errors.NameTooShort("The name of the file '{}' is too short.".format(self.path))

        extension = self.path[-4:]
        if extension == ".odt":
            self.dHTML, self.id = self.genODT()

        elif extension == ".txt":
            self.dHTML, self.id = self.genTXT()

        else:
            raise Errors.BadExtension("The extension for the file '{}' cannot be processed".format(self.path))

        Article.documentCounter += 1
        localLogger.debug("Generated document number {}".format(Article.documentCounter))
        self.generated = True

        return self.dHTML

class ArticleCluster:
    def __init__(self, path):
        self.documents = []  # get all the documents

        for document in glob(path + "/*"):
            self.documents.append(Article(document))

        self.sectionName = BodyGenerator.path.basename(path)
        self.id = BodyGenerator.Page.Tags.generateID(self.sectionName + path)

    def collectHTML(self):
        dHTML = ""
        dHTMLCount = 0
        for document in self.documents:
            dHTML += document.gen()
            if dHTMLCount < len(self.documents) - 1:
                dHTML += str(BodyGenerator.Page.Tags.Div(
                    attributes={"class": "separator"}))

            dHTMLCount += 1

        h1 = BodyGenerator.Page.Tags.Hx(1, text=self.sectionName)
        header = BodyGenerator.Page.Tags.Header(text=h1)

        section = BodyGenerator.Page.Tags.Section(text=header + dHTML, attributes={"id": self.id, "class": "Closed"})

        return str(section)


localLogger.debug("Defined Document Data structures")

# Generate all the file
documentClusters = []

for File in glob(BodyGenerator.Generation.searchPath):
    localLogger.debug("Found file at: {}".format(File))
    documentClusters.append(ArticleCluster(File))

# Add all the sections

bareHTML = BodyGenerator.Page.bareHeader
beefHTML = BodyGenerator.Page.fullHeader
downHTML = BodyGenerator.Page.embedHeader

midHTML = ""

for documentCluster in documentClusters:
    midHTML += documentCluster.collectHTML()

if len(documentClusters) == 0:
    midHTML += str(BodyGenerator.Page.Tags.Hx(1, text="No documents found"))

localLogger.info("There are {} document clusters".format(len(documentClusters)))

localLogger.info("Generating TOC...")

tocHTML = ""

folderFilePairs = dict()

for documentCluster in documentClusters:

    innerHTML = str(BodyGenerator.Page.Tags.FigureImageCombo(BodyGenerator.Generation.publicFolderImageLocation,
                                                      "{}".format(documentCluster.sectionName),
                                                             attributes=
                                                      {"class": "figure Folder",
                                                       "onclick": "OpenFolder(this)",
                                                       "data-openid": str(documentCluster.id)},
                                                             imageAttributes={"class": "figure-img img-fluid"},
                                                             imageSubtextAttributes={"class": "figure-caption text-center"}
                                                             )
                    )

    tocItemsHTML = ""

    tocItemsHTML += str(BodyGenerator.Page.Tags.FigureImageCombo(BodyGenerator.Generation.publicBackImageLocation,
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
        tocItemsHTML += str(BodyGenerator.Page.Tags.FigureImageCombo(BodyGenerator.Generation.publicFileImageLocation,
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

    innerHTML += str(BodyGenerator.Page.Tags.Div(text=tocItemsHTML))

    tocHTML += str(BodyGenerator.Page.Tags.Div(text=innerHTML, attributes={"class": "FolderAndFiles"}))

nav = BodyGenerator.Page.Tags.Nav(text=tocHTML, attributes={"class": "container"})
midMain = BodyGenerator.Page.Tags.Main(text=midHTML, attributes={"class": "container"})

minFlexWrapper = BodyGenerator.Page.Tags.Div(text=nav + midMain, attributes={"class": "FlexWrapper"})

pageContainer = BodyGenerator.Page.Tags.Div(text=minFlexWrapper + BodyGenerator.Page.FooterTag, attributes={"class": "pageContainer"})

bareHTML += midHTML + BodyGenerator.Page.HTMLEnd
beefHTML += str(pageContainer) + BodyGenerator.Page.HTMLEnd

if generateDownContent:  # Generate content for download
    downHTML += str(pageContainer) + "{resourcePackVarScript}" + BodyGenerator.Page.HTMLEnd

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
        try:
            fileLoc = "Public" + resourceCache[resource]
            makeResource = DataURI.from_file(fileLoc, base64=True).replace("\n", "")
        except FileNotFoundError:
            localLogger.warning("Failed to find resource locally. Embedded by page?")
            localLogger.debug("Writing temporary file")

            fileLoc = "file.tmp"
            with open(fileLoc, "wb") as file:
                file.write(BodyGenerator.Page.Tags.getHTMLContent(resourceCache[resource]))

            makeResource = DataURI.from_file(fileLoc, base64=True).replace("\n", "")

            localLogger.debug("Removing temporary file")
            removeFile(fileLoc)

        localLogger.debug("Made URI for '{}' from file in '{}'".format(resourceCache[resource], fileLoc))
        resourceCache[resource] = makeResource

    BodyGenerator.HelperFunctions.Save("logs/resourcePackDump.log", str(resourceCache))

    resourcePackVarLine = BodyGenerator.HelperFunctions.Read("PublicResources/Scripts/resourcePackVarTemplate.js")
    resourcePackVarLine = resourcePackVarLine.replace("{}", str(resourceCache))

    resourcePackVarScript = BodyGenerator.Page.Tags.HTMLElement("script", selfClosing=False, innerHTML=resourcePackVarLine)
    resourcePackVarScript = str(resourcePackVarScript)

    downHTML = downHTML.replace("{resourcePackVarScript}", resourcePackVarScript)

localLogger.info("Finishing building, writing...")

BodyGenerator.HelperFunctions.Save(BodyGenerator.Generation.MinimumPage, bareHTML)
BodyGenerator.HelperFunctions.Save(BodyGenerator.Generation.MainPage, beefHTML)

if generateDownContent:
    BodyGenerator.HelperFunctions.Save(BodyGenerator.Generation.DownloadPage, downHTML)

localLogger.info("Data written to '{}' folder".format(BodyGenerator.Generation.buildLocation))
localLogger.info("Checking bareHTML created code:")
html_validate.validateAndLog(bareHTML.encode())

if generateDownContent:
    localLogger.info("Checking downHTML created code:")
    html_validate.validateAndLog(downHTML.encode())

localLogger.info("Checking beefHTML created code:")
html_validate.validateAndLog(beefHTML.encode())

localLogger.info("Took: {}s".format(round(time() - start, 2)))
