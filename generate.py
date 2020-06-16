import glob
from odf import opendocument, text


class Document:
    wrapperTags = "<article>{}</article>"
    titleTags = "<h1>{}</h1>"
    paragraphTags = "<p>{}</p>"

    def __init__(self, path, phraseContent=False):
        self.path = path
        self.doc = None
        self.elements = {}
        self.HTML = None
        self.phrased = False

        if phraseContent:
            self.ph()

    def ph(self):
        self.doc = opendocument.load(self.path)
        title = self.doc.getElementsByType(text.Title)
        if len(title) > 0:
            self.elements["title"] = title[0]
        else:
            self.elements["title"] = "No Title"

        paragraphs = self.doc.getElementByType(text.P)

        if len(paragraphs) > 0:
            self.elements["paragraphs"] = paragraphs
        else:
            self.elements["paragraphs"] = [""]

        self.phrased = True

    def gen(self):
        if not self.phrased:
            self.ph()

        TitleHTML = self.titleTags.format(self.elements["title"])
        ParagraphHTML = ""
        for Paragraph in self.elements["paragraphs"]:
            ParagraphHTML += self.paragraphTags.format(Paragraph)

        HTML = TitleHTML + ParagraphHTML
        HTML = self.wrapperTags.format(HTML)

        self.HTML = HTML
        return HTML


class DocumentCluster:
    def __init__(self, path):
        self.documents = []
        


