import constants
from pathlib import Path
import shutil
import os
from html_utilities import HtmlElement, HtmlString

class WebsiteBuilder:
    def __init__(self, cssPathOriginal, lang):
        self.cssPathOriginal = cssPathOriginal
        self.cssPathCopy = "/".join([constants.WEBSITE_PATH, cssPathOriginal])
        self.cssHref = self.cssPathCopy.split(constants.WEBSITE_PATH)[-1]
        self.lang = lang
        self.pages = []
        return

    def addPages(self, pages):
        for page in pages:
            self.pages.append(page)
        return self

    def addHeadElement(self, htmlElement, page):
        headElement = HtmlElement("head")
        headElement << HtmlElement("title", contents = "korv")
        headElement << HtmlElement("link", properties = {
                                                    "rel":"'stylesheet'",
                                                    "type":"'text/css'",
                                                    "href":f"{self.cssHref}"})
        headElement << HtmlElement("meta", properties = {"charset":"\"UTF-8\""})
        headElement << HtmlElement("meta", properties = {
                                                    "name":"\"Description\"",
                                                    "content":f"\"{page.description}\""
                                                    })
        htmlElement << headElement
        return htmlElement

    def addBodyElement(self, htmlElement, page):
        htmlElement << (HtmlElement("body") << open(page.bodyfile, 'r').read())
        return htmlElement

    def pageToHtml(self, page):
        htmlString = HtmlString()
        htmlString << HtmlElement("!DOCTYPE html")

        htmlElement = HtmlElement("html", properties = {"lang":f"\"{self.lang}\""})
        self.addHeadElement(htmlElement, page)
        self.addBodyElement(htmlElement, page)
        
        htmlString << htmlElement

        return str(htmlString)

    def build(self):
        shutil.copyfile(self.cssPathOriginal, self.cssPathCopy)
        for page in self.pages:
            absoluteOutputFile = "/".join([constants.WEBSITE_PATH, page.relativeOutputFile])
            open(absoluteOutputFile, 'w').write(self.pageToHtml(page))

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
