import constants
import shutil
import os
from WebsiteBuilder import WebsiteBuilder
from ContentBuilder import HtmlElement, ContentBuilder

class Page:
    def __init__(self, title, description, bodyfile, relativeOutputFile):
        self.title = title
        self.description = description
        self.bodyfile = bodyfile
        self.relativeOutputFile = relativeOutputFile

if __name__ == "__main__":

    if os.path.exists(constants.WEBSITE_PATH):
        shutil.rmtree(constants.WEBSITE_PATH)

    os.mkdir(constants.WEBSITE_PATH)
    cssFiles = [dir for dir in os.listdir() if ".css" in dir]

    assert cssFiles, "no css file found"
    assert len(cssFiles) == 1, "too many css files; only one allowed"

    cssFile = cssFiles.pop()
    pages = [
                Page("korv", "korv är gött", "index.html", "index.html")
            ]
    WebsiteBuilder("style.css", "sv").addPages(pages).build()
