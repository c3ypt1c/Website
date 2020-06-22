class Page:
    import Tags  # Tags only needed for this specific section
    header = """<!DOCTYPE HTML><html><head><title>Lukasz Baldyga</title></head>{}<body>"""
    bareHeader = header.format("")

    HeadTags = []

    # Generating HTML for beef html template
    HeaderHTML = ""
    for tag in HeadTags:
        HeaderHTML += tag.gen()

    fullHeader = header.format(HeaderHTML)

    footer = """</body></html>"""


class Documents:
    wrapperTags = "<article>{}</article>"
    titleTags = "<h2>{}</h2>"
    paragraphTags = "<p>{}</p>"


class Generation:
    searchPath = "Sections/*"
