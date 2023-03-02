import constants
import shutil
import os
from WebsiteBuilder import WebsiteBuilder
from ContentBuilder import HtmlElement, ContentBuilder
import logging
import Adds
from LinkMenu import LinkMenuItem
from PageCategory import PageCategory

logging.basicConfig(format="%(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")

class Page:
    def __init__(self, title, description, bodyfile, relativeOutputFile):
        self.title = title
        self.description = description
        self.bodyfile = bodyfile
        self.relativeOutputFile = relativeOutputFile
        self.adders = []

preAdders = [Adds.DoctypeElementAdder(),
             Adds.HtmlElementAdder(),
             Adds.Direction.IN,
             Adds.HeadElementAdder()]
midAdders = [Adds.BodyElementAdder(),
             Adds.Direction.IN,
             Adds.PageContentAdder(),
             Adds.BulletLinkMenuAdder([LinkMenuItem() for i in range(5)]),
             Adds.Direction.OUT]
basicPageAdders = preAdders + midAdders

if __name__ == "__main__":

    if os.path.exists(constants.WEBSITE_PATH):
        shutil.rmtree(constants.WEBSITE_PATH)

    os.mkdir(constants.WEBSITE_PATH)
    cssFiles = [path for path in os.listdir() if ".css" in path]

    assert cssFiles, "no css file found"
    assert len(cssFiles) == 1, "too many css files; only one allowed"

    cssFile = cssFiles.pop()
    pages = [
                Page("korv", "korv är gött", "index.html", "index.html")
            ]
    rootCategory = PageCategory("Root", pages, basicPageAdders, "")
    WebsiteBuilder("style.css", "sv").addCategory(rootCategory).build()
