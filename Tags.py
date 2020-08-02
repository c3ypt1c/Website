import string
from urllib import request
import hashlib
from HelperFunctions import getLogger

localLogger = getLogger()


def generateID(text):
    return hashlib.sha512(str(text).encode()).hexdigest()


def getHTMLContent(url):
    InnerHTMLPage = request.urlopen(url)
    InnerHTML = InnerHTMLPage.read()
    InnerHTMLPage.close()

    try:
        InnerHTML = InnerHTML.decode()

    except UnicodeDecodeError:
        localLogger.warning("Returning bytes, can't decode: '{}' request".format(url))

    return InnerHTML


HTMLElementDB = {"style": {"selfClosing": False},
                 "link": {"selfClosing": True},
                 "script": {"selfClosing": False}
                 }


class HTMLElement:
    selfClosingString = string.Template("""<${elementName}$attributes/>""")
    notSelfClosingString = string.Template("""<${elementName}$attributes>$innerHTML</$elementName>""")
    attributeString = string.Template(""" $attribute="$value\"""")

    def __init__(self, elementName, selfClosing=None, attributes=None, innerHTML=""):
        """
        :type elementName: str
        :type selfClosing: bool
        :type attributes: dict
        :type innerHTML: str
        :type innerHTML: object

        if passing an object into innerHTML, it should be able to be represented as a string.
        """

        innerHTML = str(innerHTML)

        self.generated = False
        self.generatedContent = None

        if selfClosing is None:
            if elementName in HTMLElementDB:
                selfClosing = HTMLElementDB[elementName]["selfClosing"]
                # Add other attributes that are needed here
            else:
                localLogger.warning("Assuming that tag {} is not self closing".format(elementName))
                selfClosing = False

        if selfClosing and innerHTML:
            ValueError("Tag cannot be self closing and have inner HTML")

        self.elementName = elementName

        if attributes is None:
            attributes = {}

        self.attributes = attributes
        self.selfClosing = selfClosing
        self.innerHTML = innerHTML

    def __str__(self):
        """
        :rtype: str
        """
        if self.generated:
            return self.generatedContent

        attributesPile = ""

        for attributeName in self.attributes:
            attributesPile += self.attributeString.substitute(attribute=attributeName,
                                                              value=self.attributes[attributeName])
        if self.selfClosing:
            HTML = self.selfClosingString
            self.generatedContent = HTML.substitute(elementName=self.elementName,
                                                    attributes=attributesPile)
        else:
            HTML = self.notSelfClosingString
            self.generatedContent = HTML.substitute(elementName=self.elementName,
                                                    attributes=attributesPile,
                                                    innerHTML=self.innerHTML)

        self.generated = True
        return self.generatedContent

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return str(self) + str(other)


class Style(HTMLElement):
    def __init__(self, url, embed=False, integrity=False, external=False):
        self.generated = False
        self.generatedContent = None

        if integrity and not external:
            NotImplementedError("Integrity checking for internal files is not possible yet")  # TODO

        if embed:
            localLogger.warning("It's impossible to embed and have integrity checks. Disabling integrity checking")
            integrity = False

            InnerHTML = getHTMLContent(url)

            super(Style, self).__init__("style", selfClosing=False, innerHTML=InnerHTML)

        else:
            attributeList = {"href": url,
                             "rel": "stylesheet"
                             }

            if integrity:
                attributeList["integrity"] = integrity
                attributeList["crossorigin"] = "anonymous"

            super(Style, self).__init__("link", selfClosing=True, attributes=attributeList)


class Script(HTMLElement):
    def __init__(self, url, embed=False, integrity=False, external=False):
        if embed:
            if integrity:
                localLogger.warning("It's impossible to embed and have integrity checks. Disabling integrity checking")
                integrity = False

            InnerHTML = getHTMLContent(url)

            super(Script, self).__init__("script", selfClosing=False, innerHTML=InnerHTML)

        elif integrity and not external:
            NotImplementedError("Integrity checking for internal files is not possible yet")  # TODO

        else:
            super(Script, self).__init__("script", selfClosing=False, attributes={"src": url})
            # TODO: Script also needs integrity
            # TODO: Script also needs embedded scripts


class Paragraph(HTMLElement):
    def __init__(self, text, attributes=None):
        super(Paragraph, self).__init__("p", selfClosing=False, innerHTML=text, attributes=attributes)


class Div(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Div, self).__init__("div", selfClosing=False, innerHTML=text, attributes=attributes)


class Article(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Article, self).__init__("article", selfClosing=False, innerHTML=text, attributes=attributes)


class Section(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Section, self).__init__("section", selfClosing=False, innerHTML=text, attributes=attributes)


class Header(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Header, self).__init__("header", selfClosing=False, innerHTML=text, attributes=attributes)


class Hx(HTMLElement):
    def __init__(self, level, text="", attributes=None):
        """
        :type level: int
        level can be 1,2,3,4,5,6
        """
        if level > 6 or level < 1:
            ValueError("tag h" + str(level) + " doesn't exist.")

        super(Hx, self).__init__("h" + str(level), selfClosing=False, innerHTML=text, attributes=attributes)


class Body(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Body, self).__init__("body", selfClosing=False, innerHTML=text, attributes=attributes)


class Main(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Main, self).__init__("main", selfClosing=False, innerHTML=text, attributes=attributes)


class Nav(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Nav, self).__init__("nav", selfClosing=False, innerHTML=text, attributes=attributes)


class Image(HTMLElement):
    def __init__(self, url, attributes=None):  # Support embedding
        if attributes is None:
            attributes = {}

        attributes["src"] = url

        super(Image, self).__init__("img", selfClosing=True, attributes=attributes)


class Figure(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Figure, self).__init__("figure", selfClosing=False, innerHTML=text, attributes=attributes)


class FigCaption(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(FigCaption, self).__init__("figcaption", selfClosing=False, innerHTML=text, attributes=attributes)


class FigureImageCombo(Figure):
    def __init__(self, imageURL, imageSubtext, imageAttributes=None, imageSubtextAttributes=None, attributes=None):
        image = Image(imageURL, attributes=imageAttributes)
        figureText = FigCaption(text=imageSubtext, attributes=imageSubtextAttributes)
        super(FigureImageCombo, self).__init__(text=image+figureText, attributes=attributes)


class Title(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Title, self).__init__("title", selfClosing=False, innerHTML=text, attributes=attributes)


class Meta(HTMLElement):
    def __init__(self, attributes=None):
        super(Meta, self).__init__("meta", selfClosing=True, attributes=attributes)


class Head(HTMLElement):
    def __init__(self, text="", attributes=None):
        super(Head, self).__init__("head", selfClosing=False, innerHTML=text, attributes=attributes)


localLogger.debug("Phrased Tags.py fully")
