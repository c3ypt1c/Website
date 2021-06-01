from glob import glob
from os import path

import HelperFunctions
import Errors
import ModuleManager
import Tags
import Settings

localLogger = HelperFunctions.getLogger()


class Article:
    documentCounter = 0

    def __init__(self, documentPath, genContent=False):
        self.path = documentPath
        self.dHTML = None
        self.generated = False
        self.id = None

        self.title = ""

        if genContent:
            self.gen()

    def genODT(self):
        doc = ModuleManager.opendocument.load(self.path)

        internalArticleText = ""

        # Discover and set elements
        for element in doc.getElementsByType(ModuleManager.text.P):
            styleType = element.attributes[('urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'style-name')]
            localLogger.debug(styleType + " for " + str(element))
            if str(element).strip() == "":
                localLogger.debug("Skipping empty string")
                continue

            if styleType == "Title":
                self.title = str(element)
                internalArticleText += str(Tags.Hx(2, text=element))
            elif styleType == "P3" or styleType == "Subtitle":
                internalArticleText += str(
                    Tags.Hx(5, text=element, attributes={"class": "subtitle"}))
            else:
                internalArticleText += str(Tags.Paragraph(text=element))

        articleId = Tags.generateID(self.title + internalArticleText + str(Article.documentCounter))

        article = Tags.Article(text=internalArticleText,
                               attributes={"id": articleId}
                               )

        return str(article), articleId

    def __getRawData(self):
        with open(self.path) as f:
            fileData = f.read()

        fileData = [x.strip() for x in fileData.splitlines()]

        if len(fileData) < 2:
            raise Errors.FileTooShort("The file at '{}' has less than 2 lines".format(self.path))

        return fileData

    def genTXT(self):
        fileData = self.__getRawData()

        self.title = fileData[0]
        internalArticleText = Tags.Hx(2, self.title)

        for line in fileData[1:]:
            internalArticleText += str(Tags.Paragraph(text=line))

        articleId = Tags.generateID(
            self.title + str(internalArticleText) + str(Article.documentCounter))
        article = Tags.Article(text=internalArticleText,
                               attributes={"id": articleId}
                               )

        return str(article), articleId

    def genHTML(self):
        fileData = self.__getRawData()

        self.title = fileData[0]
        internalArticleText = Tags.Hx(2, self.title)

        internalArticleText += "".join(fileData[1:])

        articleId = Tags.generateID(
            self.title + str(internalArticleText) + str(Article.documentCounter))
        article = Tags.Article(text=internalArticleText,
                               attributes={"id": articleId}
                               )

        return str(article), articleId

    def gen(self):
        if self.generated:
            return self.dHTML

        if len(self.path) < len(".xyz"):
            raise Errors.NameTooShort("The name of the file '{}' is too short.".format(self.path))

        extension = self.path[-4:]  # TODO: Fix for extensions of different sizes
        if extension == ".odt" and ModuleManager.generateODF:
            self.dHTML, self.id = self.genODT()

        elif extension == ".txt":
            self.dHTML, self.id = self.genTXT()

        elif extension == "html" or extension == ".htm":
            self.dHTML, self.id = self.genHTML()

        else:
            raise Errors.BadExtension("The extension ('{}') for the file '{}' cannot be processed".format(extension, self.path))

        Article.documentCounter += 1
        localLogger.debug("Generated document number {}".format(Article.documentCounter))
        self.generated = True

        return self.dHTML


class ArticleCluster:
    def __init__(self, documentPath):
        self.documents = []  # get all the documents

        for document in sorted(glob(documentPath + "/*")):
            localLogger.info("Adding: {}".format(document))
            self.documents.append(Article(document))

        self.sectionName = path.basename(documentPath)

        self.id = Tags.generateID(self.sectionName + documentPath)

        if self.sectionName == Settings.Behaviour.autoOpenSection:
            self.openOnLoad = True
            localLogger.info("Found '{}' section and set id accordingly".format(Settings.Behaviour.autoOpenSection))
        else:
            self.openOnLoad = False

    def collectHTML(self):
        dHTML = ""
        dHTMLCount = 0
        for document in self.documents:
            dHTML += document.gen()
            if dHTMLCount < len(self.documents) - 1:
                dHTML += str(Tags.Div(
                    attributes={"class": "separator"}))

            dHTMLCount += 1

        h1 = Tags.Hx(1, text=self.sectionName)
        header = Tags.Header(text=h1)

        section = Tags.Section(text=header + dHTML, attributes={"id": self.id, "class": "Closed"})

        return str(section)
