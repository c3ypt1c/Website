import os
import config
from time import time
import HelperFunctions
from glob import glob
from odf import opendocument, text

start = time()
localLogger = HelperFunctions.getLogger("generate.py")
localLogger.debug("Loaded imports")


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
                self.title = str(config.Page.Tags.Hx(2, text=element))
                internalArticleText += self.title
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

        section = config.Page.Tags.Section(text=header + dHTML, attributes={"id": self.id})

        return str(section)


localLogger.debug("Defined Document Data structures")

# TODO: fix, currently Linux only
os.system("rm -r Public")
os.system("mkdir Public")
os.system("cp -r PublicResources Public/Resources")

localLogger.debug("Refreshed Public directory")

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

midMain = config.Page.Tags.Main(midHTML, attributes={"class": "container"})

bareHTML += midHTML + config.Page.footer
beefHTML += str(midMain) + config.Page.footer
downHTML += str(midMain) + config.Page.footer

localLogger.info("Finishing building, writing...")

HelperFunctions.Save("Public/bare.html", bareHTML)
HelperFunctions.Save("Public/beef.html", beefHTML)
HelperFunctions.Save("Public/down.html", downHTML)

localLogger.info("Data written")
localLogger.info("Took: {}s".format(round(time() - start, 2)))
