import HelperFunctions
from os import mkdir, remove, path  # Pycharm is a liar
import shutil
from Settings import *
from time import gmtime, strftime

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

try:
    remove("file.tmp")
    localLogger.info("Old tmp file removed")
except FileNotFoundError:
    localLogger.debug("No old file found")

localLogger.info("Rebuilding folders")
mkdir(Generation.buildLocation)

shutil.copytree("PublicResources", Generation.buildLocation + "Resources")

localLogger.debug("Refreshed Public directory at {}".format(Generation.buildLocation))


class Page:
    import Tags  # Tags only needed for this specific section
    header = """<!DOCTYPE HTML><html lang="en">{}<body {bodyAttributes}>"""
    baseHeadElementsTitle = Tags.Title("Lukasz Baldyga")
    baseHeadElementsMeta = Tags.Meta(attributes={"name": "viewport", "content": "width=device-width, initial-scale=1"})
    baseHeadElementsMeta += Tags.Meta(attributes={"charset": "utf-8"})

    # Link to favicon
    baseHeadElementsMeta += str(Tags.Link(attributes={"rel": "icon", "type": "image/png", "href": "Resources/favico.png"}))

    baseHead = Tags.Head(text=str(baseHeadElementsMeta) + str(baseHeadElementsTitle) + "{}")

    bigTitleInner = Tags.Paragraph(text="Lukasz Baldyga", attributes={"class": "Title"})
    bigTitleInner += Tags.Div(attributes={"class": "Hacker"})
    bigTitle = Tags.Div(text=bigTitleInner, attributes={"class": "TitleWrapper"})

    # Add NoScript warning
    bigTitle += Tags.NoScript(
        text="Folders won't work unless you enable JavaScript. Maybe you're looking for the <a href=bare.html class=text-success>bare</a> version?",
        attributes={"class": "text-center font-weight-bold w-100 p-3 mx-auto d-block"})

    header += str(bigTitle)

    HeadTags = [
        Tags.Script(url="https://code.jquery.com/jquery-3.5.1.slim.min.js", integrity=True),
        Tags.Script(url="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js", integrity=True),
        Tags.Style(url="https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/darkly/bootstrap.min.css"),
        Tags.Script(url="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js", integrity=True),
        Tags.Style(url="Resources/Styles/style.css", internalPath="PublicResources/Styles/style.css"),
        Tags.Script(url="Resources/Scripts/pageControl.js", integrity=True,
                    internalPath="PublicResources/Scripts/pageControl.js"),
        Tags.Script(url="Resources/Scripts/page.js", integrity=True,
                    internalPath="PublicResources/Scripts/page.js")
    ]

    EmbedHeadTags = [
        Tags.Script("https://code.jquery.com/jquery-3.5.1.slim.min.js", embed=True),
        Tags.Script("https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js", embed=True),
        Tags.Style("https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/darkly/bootstrap.min.css", embed=True),
        Tags.Script("https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js", embed=True),
        Tags.Style(internalPath="PublicResources/Styles/style.css", embed=True),
        Tags.Style(internalPath="PublicResources/Styles/styleEmbed.css", embed=True),
        Tags.Script(internalPath="PublicResources/Scripts/pageControl.js", embed=True),
        Tags.Script(internalPath="PublicResources/Scripts/resourcePack.js", embed=True),
        Tags.Script(internalPath="PublicResources/Scripts/page.js", embed=True)
    ]

    localLogger.debug("Generating HTML for beef html template")
    HeaderHTML = ""
    for tag in HeadTags:
        localLogger.debug("Adding tag with url: " + tag.getResourceInfo())
        HeaderHTML += str(tag)

    localLogger.debug("Generating HTML for down template")
    EmbedHTML = ""
    for tag in EmbedHeadTags:
        localLogger.debug("Embedding tag with resource: " + tag.getResourceInfo())
        EmbedHTML += str(tag)

    downloadHeader = header.format(baseHead, bodyAttributes="onLoad='onLoadCompressed()'")
    header = header.format(baseHead, bodyAttributes="onLoad='onLoad()'")

    fullHeader = header.format(HeaderHTML)
    embedHeader = downloadHeader.format(EmbedHTML)
    bareHeader = header.format("")

    # Increment build number
    buildNumber = 1 + int(HelperFunctions.Read(Generation.buildNumberLocation))
    HelperFunctions.Save(Generation.buildNumberLocation, str(buildNumber))

    localLogger.debug("Current build number: {}".format(buildNumber))

    # Add build number to footer
    buildNumberParagraph = Tags.Paragraph("Build Number: " + str(buildNumber))
    buildNumberParagraph += str(Tags.Paragraph("Last updated: " + strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    buildNumberParagraph += str(Tags.HTMLElement("a",
                                                 selfClosing=False,
                                                 attributes={"href": "down.html", "target": "_blank"},
                                                 pattributes=["download"],
                                                 innerHTML="Download latest page"))

    FooterDiv = Tags.Div(text=buildNumberParagraph,
                         attributes={"class": "container"})

    FooterTag = Tags.HTMLElement("footer",
                                 selfClosing=False,
                                 innerHTML=FooterDiv,
                                 attributes={"class": "footer"}
                                 )

    HTMLEnd = "</body></html>"
