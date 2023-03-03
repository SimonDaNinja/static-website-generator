import constants
import shutil
import os
from WebsiteBuilder import WebsiteBuilder
from ContentBuilder import HtmlElement, ContentBuilder
import logging
import Adds
from LinkMenu import LegacySoffanTopbarMenuElement, LinkMenuItem
from PageCategory import PageCategory
from Page import Page, CategoryPage

logging.basicConfig(format="%(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")#, level=logging.DEBUG)


if __name__ == "__main__":

    if os.path.exists(constants.WEBSITE_PATH):
        shutil.rmtree(constants.WEBSITE_PATH)

    os.mkdir(constants.WEBSITE_PATH)
    cssFiles = [path for path in os.listdir() if ".css" in path]

    assert cssFiles, "no css file found"
    assert len(cssFiles) == 1, "too many css files; only one allowed"

    cssFile = cssFiles.pop()
    #root category
    korvPage = Page("Detta är en korvhemsida om korvar", "Korv", "Korv är gött", "index.html", "index.html")
    rootPages = [korvPage]
    rootCategory = PageCategory("Root", rootPages, "")

    #foreign sausage category
    kielbasaPage = Page("Detta är en korvhemsida om kielbasa", "Kielbasa", "Kielbasa är gött", "kielbasa.html", "kielbasa.html")
    foreignSausageCategory = PageCategory("Utländsk korv", [kielbasaPage], "utländsk korv", superCategory = rootCategory)

    #chorizo category
    chiliChorizoPage = Page("Detta är en korvhemsida om chilichorizo", "Chilichorizo", "Chilichorizo är gött", "chilichorizo.html", "chilichorizo.html")
    ostChorizoPage = Page("Detta är en korvhemsida om ostchorizo", "Ostchorizo", "Ostchorizo är gött", "ostchorizo.html", "ostchorizo.html")
    chorizoCategory = PageCategory("Chorizo", [chiliChorizoPage, ostChorizoPage], "chorizo", superCategory = foreignSausageCategory)

    #add chorizo page to foreign sausage category
    chorizoPage = CategoryPage(chorizoCategory, "Sidor om chorizo", chorizoCategory.categoryName, "chorizo är gött", "chorizo.html")
    foreignSausageCategory.addPage(chorizoPage)

    #category category
    foreignSausagePage = CategoryPage(foreignSausageCategory, "Sidor om utländsk korv", foreignSausageCategory.categoryName, "Utländsk korv är gött", "utländsk korv.html")
    categoryPageCategory = PageCategory("Kategorisidor", [foreignSausagePage], "")

    topMenuOptions = [LinkMenuItem(korvPage.briefTitle, "/"),
                      LinkMenuItem(foreignSausagePage.briefTitle, foreignSausagePage.getUrl(categoryPageCategory))]

    basicPageAdders = [Adds.DoctypeElementAdder(),
                       Adds.HtmlElementAdder(),
                       Adds.Direction.IN,       # into HTML element
                       Adds.HeadElementAdder(),
                       Adds.BodyElementAdder(),
                       Adds.Direction.IN,       # into body element
                       Adds.WebsiteFullTitleH1Adder(),
                       Adds.LinkMenuAdder(topMenuOptions, LinkMenuElementClass = LegacySoffanTopbarMenuElement),
                       Adds.NavigationHelperAdder(),
                       Adds.PageFullTitleH2Adder(),
                       Adds.CategoryBriefMenuAdder(),
                       Adds.PageContentAdder(),
                       Adds.Direction.OUT]      # out from body element

    rootCategory.addAdders(basicPageAdders)
    foreignSausageCategory.addAdders(basicPageAdders)
    categoryPageCategory.addAdders(basicPageAdders)
    chorizoCategory.addAdders(basicPageAdders)
    WebsiteBuilder("style.css", "sv", "🌭Simons korvar", "🌭Simons korvar") \
        .addCategory(rootCategory) \
        .addCategory(foreignSausageCategory) \
        .addCategory(chorizoCategory) \
        .addCategory(categoryPageCategory).build()
