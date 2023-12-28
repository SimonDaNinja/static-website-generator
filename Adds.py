from .LinkMenu import BulletLinkMenuElement, LinkMenuItem, LinkMenuElement
from .ContentBuilder import HtmlElement, StringElement, NullElement
from enum import Enum, auto
from .Page import CategoryPage, RssPage
import logging

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
        headElement << HtmlElement("title", contents = f"{page.externalTitle} | {websiteBuilder.externalTitle}")
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
    def __init__(self, category = None, LinkMenuElementClass = DefaultLinkMenuElement, **kwargs):
        super().__init__(menuItems = list(), LinkMenuElementClass = LinkMenuElementClass, **kwargs)
        self.category = category

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
            title = page.externalTitle
            self.menuItems.append(LinkMenuItem(title,
                                               page.getUrl(menuCategory)))
            logging.debug(f"adding {title} to menu items")
        return super().add(page, websiteBuilder, category)


class HtmlElementAdder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("html", properties = {"lang":f"\"{websiteBuilder.lang}\""})

class DoctypeElementAdder(Adder):
    def __init__(self, *args, doctype = 'html', **kwargs):
        self.doctype = doctype

    def add(self, page, websiteBuilder, category):
        return HtmlElement(f"!DOCTYPE {self.doctype}")

class PageTitleH1Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h1", [page.internalTitle])

class PageTitleH2Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h2", [page.internalTitle])

class PageTitleH3Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h3", [page.internalTitle])

class WebsiteTitleH1Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h1", [websiteBuilder.internalTitle])

class WebsiteTitleH2Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h2", [websiteBuilder.internalTitle])

class WebsiteTitleH3Adder(Adder):
    def add(self, page, websiteBuilder, category):
        return HtmlElement("h3", [websiteBuilder.internalTitle])

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
            link << StringElement(currentPage.externalTitle)
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
        paragraphElement << StringElement(page.externalTitle)
        return paragraphElement

# Adders for RSS feed
class XmlElementAdder(Adder):
    def add(self, page, websiteBuilder, category):
        return StringElement("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>")
class RssElementAdder(Adder):
    def add(self, page, websiteBuilder, category):
        if not isinstance(page, RssPage):
            return NullElement()
        return HtmlElement("rss", properties = {"version":f"\"2.0\""})

class RssChannelElementAdder(Adder):
    def add(self, page, websiteBuilder, category):
        if not isinstance(page, RssPage):
            return NullElement()
        rssChannelElement = HtmlElement("channel")
        rssChannelElement << RssChannelTitleElementAdder().add(page, websiteBuilder, category)
        rssChannelElement << RssChannelLinkElementAdder().add(page, websiteBuilder, category)
        rssChannelElement << RssChannelDescriptionElementAdder().add(page, websiteBuilder, category)
        rssItem = page.getNextItem()
        while rssItem is not None:
            rssItemElement = HtmlElement("item")
            rssItemElement << HtmlElement("title", contents = rssItem.getTitle())
            rssItemElement << HtmlElement("link", contents = f"https://{websiteBuilder.domainName}/{rssItem.getLink()}")
            rssItemElement << HtmlElement("guid", contents = rssItem.getGuid(), properties = {"isPermaLink": "\"false\""})
            rssItemElement << HtmlElement("pubDate", contents = rssItem.getPubDate())

            descriptionElement = HtmlElement("description")
            descriptionElement << StringElement(rssItem.getDescription())

            rssItemElement << descriptionElement

            rssChannelElement << rssItemElement
            rssItem = page.getNextItem()
        page.resetItemIndex()
        return rssChannelElement

class RssChannelTitleElementAdder(Adder):
    def add(self, page, websiteBuilder, category):
        if not isinstance(page, RssPage):
            return NullElement()
        return HtmlElement("title", contents = f"{websiteBuilder.externalTitle}")

class RssChannelDescriptionElementAdder(Adder):
    def add(self, page, websiteBuilder, category):
        if not isinstance(page, RssPage):
            return NullElement()
        return HtmlElement("description", contents = f"{websiteBuilder.description}")

class RssChannelLinkElementAdder(Adder):
    def add(self, page, websiteBuilder, category):
        if not isinstance(page, RssPage):
            return NullElement()
        return HtmlElement("link", contents = f"https://{websiteBuilder.domainName}")

