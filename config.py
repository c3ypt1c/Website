class Page:
    import Tags  # Tags only needed for this specific section
    header = """<!DOCTYPE HTML><html><head><title>Lukasz Baldyga</title>{}</head><body>"""
    bareHeader = header.format("")

    HeadTags = [
        Tags.Script("https://code.jquery.com/jquery-3.5.1.slim.min.js"),
        Tags.Script("https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"),
        Tags.Style("https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css",
                   integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk",
                   external=True),
        Tags.Script("https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js")
    ]

    EmbedHeadTags = [
        Tags.Script("https://code.jquery.com/jquery-3.5.1.slim.min.js", embed=True)
    ]

    # Generating HTML for beef html template
    HeaderHTML = ""
    for tag in HeadTags:
        HeaderHTML += tag.gen()

    EmbedHTML = ""
    for tag in EmbedHeadTags:
        EmbedHTML += tag.gen()

    fullHeader = header.format(HeaderHTML)
    embedHeader = header.format(EmbedHTML)

    footer = """</body></html>"""


class Documents:
    wrapperTags = "<article>{}</article>"
    titleTags = "<h2>{}</h2>"
    subTitleTags = "<h5 class='subtitle'>{}</h5>"
    paragraphTags = "<p>{}</p>"


class Generation:
    searchPath = "Sections/*"
