import glob
from odf import opendocument, text


class Document:
    wrapperTags = "<article>{}</article>"
    titleTags = "<h1>{}</h1>"
    paragraphTags = "<p>{}</p>"

    def __init__(self, path, phraseContent=False, genContent=False):
        self.path = path
        self.doc = None
        self.elements = {}
        self.dHTML = None
        self.phrased = False
        self.generated = False

        if phraseContent:
            self.ph()

        if genContent:
            self.gen()

    def ph(self):
        self.doc = opendocument.load(self.path)
        title = self.doc.getElementsByType(text.Title)
        if len(title) > 0:
            self.elements["title"] = title[0]
        else:
            self.elements["title"] = "No Title"

        paragraphs = self.doc.getElementsByType(text.P)

        if len(paragraphs) > 0:
            self.elements["paragraphs"] = paragraphs
        else:
            self.elements["paragraphs"] = [""]

        self.phrased = True

    def gen(self):
        if not self.phrased:
            self.ph()
        elif self.generated:
            return self.dHTML

        TitleHTML = self.titleTags.format(self.elements["title"])
        ParagraphHTML = ""
        for Paragraph in self.elements["paragraphs"]:
            ParagraphHTML += self.paragraphTags.format(Paragraph)

        dHTML = TitleHTML + ParagraphHTML
        dHTML = self.wrapperTags.format(dHTML)
        self.dHTML = dHTML

        self.generated = True

        return dHTML


class DocumentCluster:
    wrapper = "<section>{}</section>"

    def __init__(self, path):
        self.documents = []

        for document in glob.glob(path + "/*"):
            self.documents.append(Document(document))

    def collectHTML(self):
        dHTML = ""
        for document in self.documents:
            dHTML += document.gen()

        dHTML = self.wrapper.format(dHTML)

        return dHTML


documentClusters = []

for File in glob.glob("Sections/*"):
    documentClusters.append(DocumentCluster(File))

# Add all the sections

HTML = "<html><head><title>Lukasz Baldyga</title></head><body>"

for documentCluster in documentClusters:
    HTML += documentCluster.collectHTML()

HTML += "</body></html>"

f = open("Public/bare.html", "w")
f.write(HTML)
f.close()
