from LinkMenu import BulletLinkMenuElement, LinkMenuItem, LinkMenuElement
from ContentBuilder import HtmlElement, StringElement
from enum import Enum, auto

class Direction(Enum):
    IN = auto()
    OUT = auto()

class Adder:
    def __init__(self):
        return

    def add(self, page, websiteBuilder):
        return HtmlElement("p")

class HeadElementAdder(Adder):
    def add(self, page, websiteBuilder):
        headElement = HtmlElement("head")
        headElement << HtmlElement("title", contents = "korv")
        headElement << HtmlElement("link", properties = {
                                                    "rel":"'stylesheet'",
                                                    "type":"'text/css'",
                                                    "href":f"{websiteBuilder.cssHref}"})
        headElement << HtmlElement("meta", properties = {"charset":"\"UTF-8\""})
        headElement << HtmlElement("meta", properties = {
                                                    "name":"\"Description\"",
                                                    "content":f"\"{page.description}\""
                                                    })
        return headElement

class BodyElementAdder(Adder):
    def add(self, page, websiteBuilder):
        return HtmlElement("body")

class PageContentAdder(Adder):
    def add(self, page, websiteBuilder):
        return StringElement(open(page.bodyfile, 'r').read())

class LinkMenuAdder(Adder):
    def __init__(self, menuItems, *args, LinkMenuElementClass = LinkMenuElement, **kwargs):
        super().__init__(*args, **kwargs)
        self.menuItems = menuItems
        self.LinkMenuElementClass = LinkMenuElementClass

    def add(self, page, websiteBuilder):
        return self.LinkMenuElementClass(self.menuItems)

class BulletLinkMenuAdder(LinkMenuAdder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, LinkMenuElementClass = BulletLinkMenuElement, **kwargs)

class HtmlElementAdder(Adder):
    def add(self, page, websiteBuilder):
        return HtmlElement("html", properties = {"lang":f"\"{websiteBuilder.lang}\""})

class DoctypeElementAdder(Adder):
    def __init__(self, *args, doctype = 'html', **kwargs):
        self.doctype = doctype

    def add(self, page, websiteBuilder):
        return HtmlElement(f"!DOCTYPE {self.doctype}")

