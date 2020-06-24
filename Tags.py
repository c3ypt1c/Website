import string

# from abc import abstractmethod
# Temporarily commented as it might be needed for other classes

HTMLElementDB = {"style": {"selfClosing": False},
                 "link": {"selfClosing": True},
                 "script": {"selfClosing": False}
                 }


class HTMLElement:  # TODO: Optimise eHTML variable
    selfClosingString = string.Template("""<${elementName}$attributes/>""")
    notSelfClosingString = string.Template("""<${elementName}$attributes></$elementName>""")  # TODO: InnerHTML
    attributeString = string.Template(""" $attribute=\"$value\"""")

    def __init__(self, elementName, selfClosing=None, attributes=None):
        """
        :type elementName: str
        :type selfClosing: bool
        :type attributes: dict
        """

        self.generated = False
        self.generatedContent = None
        self.eHTML = None

        if selfClosing is None:
            if elementName in HTMLElementDB:
                selfClosing = HTMLElementDB[elementName]["selfClosing"]  # Add other attributes that are needed here
            else:
                # TODO: Log here that it is assuming that it's not self closing
                selfClosing = False

        self.elementName = elementName

        if attributes is None:
            attributes = {}

        self.attributes = attributes
        self.selfClosing = selfClosing

    def gen(self):
        """
        :rtype: str
        """
        if self.generated:
            return self.generatedContent

        if self.selfClosing:
            self.eHTML = self.selfClosingString
        else:
            self.eHTML = self.notSelfClosingString

        attributesPile = ""

        for attributeName in self.attributes:
            attributesPile += self.attributeString.substitute(attribute=attributeName,
                                                              value=self.attributes[attributeName])

        self.generatedContent = self.eHTML.substitute(elementName=self.elementName, attributes=attributesPile)
        self.generated = True
        return self.generatedContent


class Style(HTMLElement):
    def __init__(self, url, embed=False, integrity=False, external=False):

        if embed:
            NotImplementedError("Embedding CSS directly is not implemented yet")  # TODO

        elif integrity and not external:
            NotImplementedError("Integrity checking for internal files is not possible yet")  # TODO

        else:
            attributeList = {"src": url}
            if integrity:
                attributeList["integrity"] = integrity
                attributeList["crossorgin"] = "anonymous"
            super(Style, self).__init__("link", selfClosing=True, attributes=attributeList)


class Script(HTMLElement):
    def __init__(self, url):
        super(Script, self).__init__("script", selfClosing=False, attributes={"src": url})
        # TODO: Script also needs integrity
        # TODO: Script also needs embedded scripts
