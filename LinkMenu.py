import ContentBuilder

class LinkMenuElement(ContentBuilder.ContentElement):
    def __init__(self, menuItems):
        self.menuItems = menuItems

class BulletLinkMenuElement(LinkMenuElement):
    def addSelf(self, builder):
        listElement = ContentBuilder.HtmlElement("ul")
        for item in self.menuItems:
            listItemElement = ContentBuilder.HtmlElement("li")
            listItemElement << item.getLinkElement()
            listElement << listItemElement
        builder << listElement

class LinkMenuItem:
    def __init__(self, text, href):
        self.text = text
        self.href = href

    def getLinkElement(self):
        linkElement = ContentBuilder.HtmlElement("a")
        linkElement << {"href": f"'{self.href}'"}
        linkElement << ContentBuilder.StringElement(self.text)
        return linkElement

