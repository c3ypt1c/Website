import os
import config
# import logging  #  TODO
import HelperFunctions
from glob import glob
from odf import opendocument, text


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

        section = config.Page.Tags.Section(text=header+dHTML, attributes={"id": self.id})

        return str(section)


# TODO: fix, currently Linux only
os.system("rm -r Public")
os.system("mkdir Public")
os.system("cp -r PublicResources Public/Resources")

# Generate all the file
documentClusters = []

for File in glob(config.Generation.searchPath):
    documentClusters.append(DocumentCluster(File))

# Add all the sections

bareHTML = config.Page.bareHeader
beefHTML = config.Page.fullHeader
downHTML = config.Page.embedHeader

midHTML = ""

for documentCluster in documentClusters:
    midHTML += documentCluster.collectHTML()

if len(documentClusters) == 0:
    midHTML += "<h1>No documents found</h1>"

bareHTML += midHTML + config.Page.footer
beefHTML += midHTML + config.Page.footer
downHTML += midHTML + config.Page.footer

HelperFunctions.Save("Public/bare.html", bareHTML)
HelperFunctions.Save("Public/beef.html", beefHTML)
HelperFunctions.Save("Public/down.html", downHTML)
