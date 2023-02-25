import ContentBuilder

class LinkMenuElement(ContentBuilder.ContentElement):
    def __init__(self, menuItems):
        self.menuItems = menuItems

class BulletLinkMenuElement(LinkMenuElement):
    def addSelf(self, builder):
        listElement = ContentBuilder.HtmlElement("ul")
        for item in self.menuItems:
            listItemElement = ContentBuilder.HtmlElement("li")
            listItemElement << item.getFull()
            listElement << listItemElement
        builder << listElement

class LinkMenuItem:
    def __init__(self):
        return

    def getFull(self):
        linkElement = ContentBuilder.HtmlElement("a")
        linkElement << {"href": "/"}
        linkElement << ContentBuilder.StringElement("🚧 - ABSTRACT_MENU_ITEM - 🚧")
        return linkElement

    def getBrief(self):
        return self.getFull()

