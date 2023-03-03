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
    def __init__(self, title, description, bodyfile, fileName):
        self.title = title
        self.description = description
        self.bodyfile = bodyfile
        self.fileName = fileName

    def getRelativeOutputFile(self, category):
        return "/".join([category.relativeOutputDir, self.fileName])

preAdders = [Adds.DoctypeElementAdder(),
             Adds.HtmlElementAdder(),
             Adds.Direction.IN, # into HTML element
             Adds.HeadElementAdder()]
midAdders = [Adds.BodyElementAdder(),
             Adds.Direction.IN, # into body element
             Adds.PageContentAdder()] 
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
                Page("korv", "korv är gött", "index.html", "index.html"),
                Page("kielbasa", "kielbasa är gött", "kielbasa.html", "kielbasa.html"),
                Page("chorizo", "chorizo är gött", "chorizo.html", "chorizo.html")
            ]
    rootCategory = PageCategory("Root", pages, basicPageAdders, "")
    rootCategory.addAdder(Adds.CategoryMenuAdder(rootCategory))
    rootCategory.addAdder(Adds.Direction.OUT) # out from body element
    WebsiteBuilder("style.css", "sv").addCategory(rootCategory).build()
