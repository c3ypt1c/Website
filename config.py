import HelperFunctions
from os import mkdir, path
import shutil
from StaticStrings import *

# remove old log
shutil.rmtree(Logging.loggerFolder)
mkdir(Logging.loggerFolder)

localLogger = HelperFunctions.getLogger()
localLogger.debug("Rebuilt logging directory")

# Removing paths
try:
    localLogger.info("Removing old folder: " + Generation.buildLocation)
    shutil.rmtree(Generation.buildLocation)
    localLogger.info("Removed successfully")
except FileNotFoundError:
    localLogger.warning("Folder not found. Ignore this if this is the first time building.")

localLogger.info("Rebuilding folders")
mkdir(Generation.buildLocation)

shutil.copytree("PublicResources", Generation.buildLocation + "Resources")

localLogger.debug("Refreshed Public directory at {}".format(Generation.buildLocation))


class Page:
    import Tags  # Tags only needed for this specific section
    header = """<!DOCTYPE HTML><html>{}<body{bodyAttributes}>"""
    baseHeadElementsTitle = Tags.Title("Lukasz Baldyga")
    baseHeadElementsMeta = Tags.Meta(attributes={"name": "viewport", "content": "width=device-width, initial-scale=1"})
    baseHeadElementsMeta += Tags.Meta(attributes={"charset": "utf-8"})

    baseHead = Tags.Head(text=str(baseHeadElementsMeta) + str(baseHeadElementsTitle) + "{}")

    bigTitleInner = Tags.Paragraph(text="Lukasz Baldyga", attributes={"class": "Title"})
    bigTitleInner += Tags.Div(attributes={"class": "Hacker"})
    bigTitle = Tags.Div(text=bigTitleInner, attributes={"class": "TitleWrapper"})

    header += str(bigTitle)

    HeadTags = [
        Tags.Script("https://code.jquery.com/jquery-3.5.1.slim.min.js", integrity=True),
        Tags.Script("https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js", integrity=True),
        Tags.Style("https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/darkly/bootstrap.min.css", integrity=True),
        Tags.Script("https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js", integrity=True),
        Tags.Style("Resources/Styles/style.css", integrity=True, internalPath="PublicResources/Styles/style.css"),
        Tags.Script("Resources/Scripts/pageControl.js", integrity=True,
                    internalPath="PublicResources/Scripts/pageControl.js")
    ]

    EmbedHeadTags = [
        Tags.Script("https://code.jquery.com/jquery-3.5.1.slim.min.js", embed=True),
        Tags.Script("https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js", embed=True),
        Tags.Style("https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/darkly/bootstrap.min.css", embed=True),
        Tags.Script("https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js", embed=True),
        Tags.Style(Generation.publicFacingHTMLServerPath + "Resources/Styles/style.css", embed=True),
        Tags.Style(Generation.publicFacingHTMLServerPath + "Resources/Styles/styleEmbed.css", embed=True),
        Tags.Script(Generation.publicFacingHTMLServerPath + "Resources/Scripts/pageControl.js", embed=True),
        Tags.Script(Generation.publicFacingHTMLServerPath + "Resources/Scripts/resourcePack.js", embed=True)
    ]

    localLogger.debug("Generating HTML for beef html template")
    HeaderHTML = ""
    for tag in HeadTags:
        localLogger.debug("Adding tag with url: " + tag.url)
        HeaderHTML += str(tag)

    localLogger.debug("Generating HTML for down template")
    EmbedHTML = ""
    for tag in EmbedHeadTags:
        localLogger.debug("Embedding tag with url: " + tag.url)
        EmbedHTML += str(tag)

    downloadHeader = header.format(baseHead, bodyAttributes=" onLoad='decompress()'")
    header = header.format(baseHead, bodyAttributes="")

    fullHeader = header.format(HeaderHTML)
    embedHeader = downloadHeader.format(EmbedHTML)
    bareHeader = header.format("")

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
