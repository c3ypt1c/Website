import os
import config
from glob import glob
from odf import opendocument, text


# TODO: Logging.
# TODO: Increment build number


class Document:
    def __init__(self, path, genContent=False):
        self.path = path
        self.doc = None
        self.elements = {}
        self.dHTML = None
        self.generated = False

        if genContent:
            self.gen()

    def gen(self):
        if self.generated:
            return self.dHTML

        dHTML = ""

        self.doc = opendocument.load(self.path)

        for element in self.doc.getElementsByType(text.P):
            styleType = element.attributes[('urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'style-name')]
            if styleType == "Title":
                dHTML += config.Documents.titleTags.format(element)
            elif styleType == "P3":
                dHTML += config.Documents.subTitleTags.format(element)
            else:
                dHTML += config.Documents.paragraphTags.format(element)

        dHTML = config.Documents.wrapperTags.format(dHTML)
        self.dHTML = dHTML

        self.generated = True

        return dHTML


class DocumentCluster:
    wrapper = "<section><header><h1>{}<h1></header>{}</section>"

    def __init__(self, path):
        self.documents = []  # get all the documents

        for document in glob(path + "/*"):
            self.documents.append(Document(document))

        self.sectionName = os.path.basename(path)

    def collectHTML(self):
        dHTML = ""
        for document in self.documents:
            dHTML += document.gen()

        dHTML = self.wrapper.format(self.sectionName, dHTML)

        return dHTML


documentClusters = []

for File in glob(config.Generation.searchPath):
    documentClusters.append(DocumentCluster(File))

# Add all the sections

bareHTML = config.Page.bareHeader
beefHTML = config.Page.fullHeader

midHTML = ""

for documentCluster in documentClusters:
    midHTML += documentCluster.collectHTML()

if len(documentClusters) == 0:
    midHTML += "<h1>No documents found</h1>"

bareHTML += midHTML + config.Page.footer
beefHTML += midHTML + config.Page.footer

f = open("Public/bare.html", "w")
f.write(bareHTML)
f.close()

f = open("Public/beef.html", "w")
f.write(beefHTML)
f.close()
