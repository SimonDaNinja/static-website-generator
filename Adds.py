from LinkMenu import BulletLinkMenuElement, LinkMenuItem, LinkMenuElement
from ContentBuilder import HtmlElement, StringElement, NullElement
from enum import Enum, auto
from Page import CategoryPage

DefaultLinkMenuElement= BulletLinkMenuElement

class Direction(Enum):
    IN = auto()
    OUT = auto()

class Adder:
    def __init__(self):
        return

    def add(self, page, websiteBuilder, category):
        return HtmlElement("p")

class HeadElementAdder(Adder):
    def add(self, page, websiteBuilder, category):
        headElement = HtmlElement("head")
        headElement << HtmlElement("title", contents = page.briefTitle)
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
    def add(self, page, websiteBuilder, category):
        return HtmlElement("body")

class PageContentAdder(Adder):
    def add(self, page, websiteBuilder, category):
        return StringElement(open(page.bodyfile, 'r').read()) if page.bodyfile is not None else NullElement()

class LinkMenuAdder(Adder):
    def __init__(self, menuItems, *args, LinkMenuElementClass = DefaultLinkMenuElement, **kwargs):
        super().__init__(*args, **kwargs)
        self.menuItems = menuItems
        self.LinkMenuElementClass = LinkMenuElementClass

    def add(self, page, websiteBuilder, category):
        return self.LinkMenuElementClass(self.menuItems)

class CategoryMenuAdder(LinkMenuAdder):
    def __init__(self, *args, category = None, brief = True, LinkMenuElementClass = DefaultLinkMenuElement, **kwargs):
        super().__init__(menuItems = list(), *args, LinkMenuElementClass = LinkMenuElementClass, **kwargs)
        self.category = category
        self.brief = brief

    def add(self, page, websiteBuilder, category):
        if self.category == None:
            if not isinstance(page, CategoryPage):
                return NullElement()
            menuCategory = page.category
        else:
            menuCategory = self.category
        preOutputFiles = {}
        self.menuItems = list()
        for page in menuCategory.pages:
            title = page.briefTitle if self.brief else page.fullTitle
            self.menuItems.append(LinkMenuItem(title,
                                               page.getUrl(menuCategory)))
        return super().add(page, websiteBuilder, category)

class CategoryFullMenuAdder(CategoryMenuAdder):
    def __init__(self, category = None, *args, LinkMenuElementClass = DefaultLinkMenuElement, **kwargs):
        super().__init__(*args, category = category, brief = False, **kwargs)
        self.category = category

class CategoryBriefMenuAdder(CategoryMenuAdder):
    def __init__(self, category = None, *args, LinkMenuElementClass = DefaultLinkMenuElement, **kwargs):
        super().__init__(*args, category = category, brief = True, **kwargs)
        self.category = category

class HtmlElementAdder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("html", properties = {"lang":f"\"{websiteBuilder.lang}\""})

class DoctypeElementAdder(Adder):
    def __init__(self, *args, doctype = 'html', **kwargs):
        self.doctype = doctype

    def add(self, page, websiteBuilder, category):
        return HtmlElement(f"!DOCTYPE {self.doctype}")

class PageFullTitleH1Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h1", [page.fullTitle])

class PageFullTitleH2Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h2", [page.fullTitle])

class PageFullTitleH3Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h3", [page.fullTitle])

class PageBriefTitleH1Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h1", [page.briefTitle])

class PageBriefTitleH2Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h2", [page.briefTitle])

class PageBriefTitleH3Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h3", [page.briefTitle])

class WebsiteFullTitleH1Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h1", [websiteBuilder.fullTitle])

class WebsiteFullTitleH2Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h2", [websiteBuilder.fullTitle])

class WebsiteFullTitleH3Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h3", [websiteBuilder.fullTitle])

class WebsiteBriefTitleH1Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h1", [websiteBuilder.briefTitle])

class WebsiteBriefTitleH2Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h2", [websiteBuilder.briefTitle])

class WebsiteBriefTitleH3Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h3", [websiteBuilder.briefTitle])

class NavigationHelperAdder(Adder):
    def add(self, page, websiteBuilder, category):
        paragraphElement = HtmlElement("p")
        separator = " &gt; "
        links = []
        currentPage = category.categoryPage 
        while True:
            if currentPage is None:
                break
            nextCategory = currentPage.category.superCategory
            link = HtmlElement("a")
            link << {"href" : currentPage.getUrl(nextCategory)}
            link << StringElement(currentPage.briefTitle)
            links.append(link)
            if nextCategory is None:
                break
            currentPage = nextCategory.categoryPage
        if not links:
            return NullElement()
        links.reverse()
        for link in links:
            paragraphElement << link
            paragraphElement << StringElement(separator)
        paragraphElement << StringElement(page.briefTitle)
        return paragraphElement

