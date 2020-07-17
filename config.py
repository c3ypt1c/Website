import HelperFunctions
from os import system
from StaticStrings import *

# remove old log TODO: fix unsafe parameter TODO: fix Linux only
system("rm -r " + Logging.loggerFolder)
system("mkdir " + Logging.loggerFolder)

localLogger = HelperFunctions.getLogger("config.py")


class Page:
    import Tags  # Tags only needed for this specific section
    header = """<!DOCTYPE HTML><html><head><title>Lukasz Baldyga</title>{}</head><body>"""
    bareHeader = header.format("")

    bigTitleInner = Tags.Paragraph(text="Lukasz Baldyga", attributes={"class": "Title"})
    bigTitleInner += Tags.Div(attributes={"class": "Hacker"})
    bigTitle = Tags.Div(text=bigTitleInner, attributes={"class": "TitleWrapper"})

    header += str(bigTitle)

    HeadTags = [
        Tags.Script("https://code.jquery.com/jquery-3.5.1.slim.min.js"),
        Tags.Script("https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"),
        Tags.Style("https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/darkly/bootstrap.min.css"),
        Tags.Script("https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"),
        Tags.Script("https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"),  # Advert Script
        Tags.Style("Resources/Styles/style.css")
    ]

    EmbedHeadTags = [
        Tags.Style("http://localhost/PublicResources/style.css"),
        Tags.Script("https://code.jquery.com/jquery-3.5.1.slim.min.js", embed=True),
        Tags.Script("https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js", embed=True),
        Tags.Style("https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/darkly/bootstrap.min.css", embed=True),
        Tags.Script("https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js", embed=True)
    ]

    # Generating HTML for beef html template
    HeaderHTML = ""
    for tag in HeadTags:
        HeaderHTML += str(tag)

    EmbedHTML = ""
    for tag in EmbedHeadTags:
        EmbedHTML += str(tag)

    fullHeader = header.format(HeaderHTML)
    embedHeader = header.format(EmbedHTML)

    # Increment build number
    buildNumber = 1 + int(HelperFunctions.Read(Generation.buildNumberLocation))
    HelperFunctions.Save(Generation.buildNumberLocation, str(buildNumber))

    localLogger.debug("Current build number: {}".format(buildNumber))

    # Add build number to footer
    buildNumberParagraph = Tags.Paragraph("Build Number: " + str(buildNumber))
    FooterDiv = Tags.Div(text=buildNumberParagraph,
                         attributes={"class": "container"})

    FooterTag = Tags.HTMLElement("footer",
                                 selfClosing=False,
                                 innerHTML=FooterDiv,
                                 attributes={"class": "footer"}
                                 )

    footer = """{}</body></html>""".format(FooterTag)
