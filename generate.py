import os
import shutil
import config
from time import time
import HelperFunctions
from glob import glob

localLogger = HelperFunctions.getLogger("generate.py")
localLogger.debug("Loaded imports")

try:
    from odf import opendocument, text
except ModuleNotFoundError:
    localLogger.error("odf module not found. Please install odfpy. Instructions: https://pypi.org/project/odfpy/")
    ModuleNotFoundError()

start = time()


class Document:
    documentCounter = 0

    def __init__(self, path, genContent=False):
        self.path = path
        self.doc = None
        self.elements = {}
        self.dHTML = None
        self.generated = False

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
        article = config.Page.Tags.Article(text=internalArticleText,
                                           attributes={"id": config.Page.Tags.generateID(self.title +
                                                                                         internalArticleText +
                                                                                         str(Document.documentCounter)
                                                                                         )
                                                       }
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

        self.sectionName = os.path.basename(path)
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

# Removing paths
try:
    localLogger.info("Removing old folder: " + config.Generation.buildLocation)
    shutil.rmtree(config.Generation.buildLocation)
    localLogger.info("Removed successfully")
except FileNotFoundError:
    localLogger.warning("Folder not found. Ignore this if this is the first time building.")

localLogger.info("Rebuilding folders")
os.mkdir(config.Generation.buildLocation)

# TODO: Fix for Windows
os.system("cp -r PublicResources {}".format(config.Generation.buildLocation + "Resources"))

localLogger.debug("Refreshed Public directory at {}".format(config.Generation.buildLocation))

# Generate all the file
documentClusters = []

for File in glob(config.Generation.searchPath):
    localLogger.info("Found file at: {}".format(File))
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
                                                              attributes={"class": "figure File Closed"},
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

bareHTML += midHTML + config.Page.footer
beefHTML += str(minFlexWrapper) + config.Page.footer
downHTML += str(minFlexWrapper) + config.Page.footer

localLogger.info("Finishing building, writing...")

HelperFunctions.Save(config.Generation.buildLocation + "bare.html", bareHTML)
HelperFunctions.Save(config.Generation.buildLocation + "beef.html", beefHTML)
HelperFunctions.Save(config.Generation.buildLocation + "down.html", downHTML)

localLogger.info("Data written to '{}' folder".format(config.Generation.buildLocation))
localLogger.info("Took: {}s".format(round(time() - start, 2)))
