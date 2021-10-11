#!/usr/bin/python
# Import time to literally time how long it takes to compile the website
from time import time

start = time()

# Python standard imports
from time import gmtime, strftime
from os import remove, mkdir
import shutil
from glob import glob

# Project imports
import HelperFunctions
import Tags
import Article

localLogger = HelperFunctions.getLogger()

# remove old log
try:
    shutil.rmtree(Article.Settings.Logging.loggerFolder)
except:
    localLogger.warning("Failed to removed old logger folder: '{}'".format(Article.Settings.Logging.loggerFolder))

mkdir(Article.Settings.Logging.loggerFolder)

localLogger.debug("Rebuilt logging directory")

# Removing paths
try:
    localLogger.info("Removing old folder: " + Article.Settings.Generation.buildLocation)
    shutil.rmtree(Article.Settings.Generation.buildLocation)
    localLogger.info("Removed successfully")
except FileNotFoundError:
    localLogger.warning("Folder not found. Ignore this if this is the first time building.")

# Removing temporary files
try:
    remove("file.tmp")
    localLogger.info("Old tmp file removed")
except FileNotFoundError:
    localLogger.debug("No old file found")

# Remaking folders
localLogger.info("Rebuilding folders")
mkdir(Article.Settings.Generation.buildLocation)

shutil.copytree("PublicResources", Article.Settings.Generation.buildLocation + "Resources")

localLogger.debug("Refreshed Public directory at {}".format(Article.Settings.Generation.buildLocation))


class Page:
    header = """<!DOCTYPE HTML><html lang="en">{}<body {bodyAttributes}>"""
    baseHeadElementsTitle = Tags.Title("Lukasz Baldyga")
    baseHeadElementsMeta = Tags.Meta(attributes={"name": "viewport", "content": "width=device-width, initial-scale=1"})
    baseHeadElementsMeta += Tags.Meta(attributes={"charset": "utf-8"})

    # Link to favicon
    baseHeadElementsMeta += str(
        Tags.Link(attributes={"rel": "icon", "type": "image/png", "href": "Resources/favico.png"}))

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
    buildNumber = 1 + int(HelperFunctions.Read(Article.Settings.Generation.buildNumberLocation))
    HelperFunctions.Save(Article.Settings.Generation.buildNumberLocation, str(buildNumber))

    localLogger.debug("Current build number: {}".format(buildNumber))

    # Add build number to footer
    buildNumberParagraph = Tags.Paragraph("Build Number: " + str(buildNumber))
    buildNumberParagraph += str(Tags.Paragraph("Last updated: " + strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    buildNumberParagraph += str(Tags.HTMLElement("a",
                                                 selfClosing=False,
                                                 attributes={"href": "https://baldy.ga/down.html", "target": "_blank"},
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


# Generate all the file
documentClusters = []

for File in sorted(glob(Article.Settings.Generation.searchPath)):
    localLogger.debug("Found file at: {}".format(File))
    documentClusters.append(Article.ArticleCluster(File))

# Add all the sections

bareHTML = Page.bareHeader
beefHTML = Page.fullHeader
downHTML = Page.embedHeader

midHTML = ""

for documentCluster in documentClusters:
    midHTML += documentCluster.collectHTML()

if len(documentClusters) == 0:
    midHTML += str(Tags.Hx(1, text="No documents found"))

localLogger.info("There are {} document clusters".format(len(documentClusters)))

localLogger.info("Generating TOC...")

tocHTML = ""

folderFilePairs = dict()

for documentCluster in documentClusters:

    documentClusterAttributes = {"class": "figure Folder", "onclick": "OpenFolder(this)",
                                 "data-openid": str(documentCluster.id)}
    if documentCluster.openOnLoad:
        documentClusterAttributes["id"] = "openThisOnLoad"

    innerHTML = str(Tags.FigureImageCombo(Article.Settings.Generation.publicFolderImageLocation,
                                          "{}".format(documentCluster.sectionName),
                                          attributes=documentClusterAttributes,
                                          imageAttributes={"class": "figure-img img-fluid"},
                                          imageSubtextAttributes={
                                              "class": "figure-caption text-center"}
                                          )
                    )

    tocItemsHTML = ""

    tocItemsHTML += str(Tags.FigureImageCombo(Article.Settings.Generation.publicBackImageLocation,
                                              "Go back",
                                              attributes=
                                              {"class": "figure File Back Closed",
                                               "onclick": "ShowAllFolders()"
                                               },
                                              imageAttributes={"class": "figure-img img-fluid"},
                                              imageSubtextAttributes={
                                                  "class": "figure-caption text-center"}
                                              )
                        )

    for documentDC in documentCluster.documents:
        tocItemsHTML += str(Tags.FigureImageCombo(Article.Settings.Generation.publicFileImageLocation,
                                                  documentDC.title,
                                                  attributes={"class": "figure File Closed",
                                                              "data-openid": str(documentDC.id),
                                                              "onclick": "OpenSection(this)"
                                                              },
                                                  imageAttributes={"class": "figure-img img-fluid"},
                                                  imageSubtextAttributes=
                                                  {"class": "figure-caption text-center"}
                                                  )
                            )

    innerHTML += str(Tags.Div(text=tocItemsHTML))

    tocHTML += str(Tags.Div(text=innerHTML, attributes={"class": "FolderAndFiles"}))

nav = Tags.Nav(text=tocHTML, attributes={"class": "container"})
midMain = Tags.Main(text=midHTML, attributes={"class": "container"})

minFlexWrapper = Tags.Div(text=nav + midMain, attributes={"class": "FlexWrapper"})

pageContainer = Tags.Div(text=minFlexWrapper + Page.FooterTag,
                         attributes={"class": "pageContainer"})

bareHTML += midHTML + Page.HTMLEnd
beefHTML += str(pageContainer) + Page.HTMLEnd

if Article.ModuleManager.generateDownContent:  # Generate content for download
    downHTML += str(pageContainer) + "{resourcePackVarScript}" + Page.HTMLEnd

    localLogger.info("Generating the downloadable version of the website")
    resourceCache = dict()
    pointer = 0
    while pointer != len(downHTML):
        nextImgTag = downHTML.find("<img ", pointer)
        if nextImgTag == -1:
            break

        localLogger.debug("Found img tag at: " + str(nextImgTag))

        srcAttributeStart = downHTML.find("src=\"", nextImgTag)

        localLogger.debug("Found src attribute in img at: " + str(srcAttributeStart))

        srcAttributeStart += len("src=\"")
        srcAttributeEnd = downHTML.find("\"", srcAttributeStart)

        localLogger.debug("Found src attribute end at: " + str(srcAttributeEnd))

        localURL = downHTML[srcAttributeStart:srcAttributeEnd]

        localLogger.debug("Full string: '{}'".format(localURL))

        if localURL not in resourceCache:
            localLogger.debug("Downloading and caching resource.")

            resourceCache[localURL] = localURL
        else:
            localLogger.debug("Resource already downloaded, skipping...")

        pointer = downHTML.find(">", nextImgTag + 1)

    localLogger.info("Making resources for download and packing them into the resource pack variable")

    for resource in resourceCache:
        try:
            fileLoc = "Public" + resourceCache[resource]
            makeResource = Article.ModuleManager.DataURI.from_file(fileLoc, base64=True).replace("\n", "")
        except FileNotFoundError:
            localLogger.warning("Failed to find resource locally. Embedded by page?")
            localLogger.debug("Writing temporary file")

            fileLoc = "file.tmp"
            with open(fileLoc, "wb") as file:
                file.write(Tags.getHTMLContent(resourceCache[resource]))

            makeResource = Article.ModuleManager.DataURI.from_file(fileLoc, base64=True).replace("\n", "")

            localLogger.debug("Removing temporary file")
            remove(fileLoc)

        localLogger.debug("Made URI for '{}' from file in '{}'".format(resourceCache[resource], fileLoc))
        resourceCache[resource] = makeResource

    HelperFunctions.Save("logs/resourcePackDump.log", str(resourceCache))

    resourcePackVarLine = HelperFunctions.Read("PublicResources/Scripts/resourcePackVarTemplate.js")
    resourcePackVarLine = resourcePackVarLine.replace("{}", str(resourceCache))

    resourcePackVarScript = Tags.HTMLElement("script", selfClosing=False,
                                             innerHTML=resourcePackVarLine)
    resourcePackVarScript = str(resourcePackVarScript)

    downHTML = downHTML.replace("{resourcePackVarScript}", resourcePackVarScript)

localLogger.info("Finishing building, writing...")

HelperFunctions.Save(Article.Settings.Generation.MinimumPage, bareHTML)
HelperFunctions.Save(Article.Settings.Generation.MainPage, beefHTML)

if Article.ModuleManager.generateDownContent:
    HelperFunctions.Save(Article.Settings.Generation.DownloadPage, downHTML)

localLogger.info("Data written to '{}' folder".format(Article.Settings.Generation.buildLocation))

if Article.Settings.Verification.verify:
    import html_validate
    # Check minimum page
    if Article.Settings.Verification.verifyMinimumPage:
        localLogger.info("Checking bareHTML created code:")
        html_validate.validateAndLog(bareHTML.encode())
    else:
        localLogger.info("Skipping verification for: bareHTML")

    # Check download page
    if Article.ModuleManager.generateDownContent and Article.Settings.Verification.verifyDownloadPage:
        localLogger.info("Checking downHTML created code:")
        html_validate.validateAndLog(downHTML.encode())
    else:
        localLogger.info("Skipping verification for: downHTML")

    # Check main page
    if Article.Settings.Verification.verifyMainPage:
        localLogger.info("Checking beefHTML created code:")
        html_validate.validateAndLog(beefHTML.encode())
    else:
        localLogger.info("Skipping verification for: beefHTML")

localLogger.info("Took: {}s".format(round(time() - start, 2)))
