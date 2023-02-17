import constants
import shutil
from ContentBuilder import HtmlElement, ContentBuilder

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
        contentBuilder = ContentBuilder()
        contentBuilder << HtmlElement("!DOCTYPE html")

        htmlElement = HtmlElement("html", properties = {"lang":f"\"{self.lang}\""})
        self.addHeadElement(htmlElement, page)
        self.addBodyElement(htmlElement, page)
        
        contentBuilder << htmlElement

        return str(contentBuilder)

    def build(self):
        shutil.copyfile(self.cssPathOriginal, self.cssPathCopy)
        for page in self.pages:
            absoluteOutputFile = "/".join([constants.WEBSITE_PATH, page.relativeOutputFile])
            open(absoluteOutputFile, 'w').write(self.pageToHtml(page))
