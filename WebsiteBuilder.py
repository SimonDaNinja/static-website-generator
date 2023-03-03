import constants
import logging
import shutil
import Adds
from ContentBuilder import HtmlElement, ContentBuilder
import logging

class WebsiteBuilder:

    def __init__(self, cssPathOriginal, lang):
        self.cssPathOriginal = cssPathOriginal
        self.cssPathCopy = "/".join([constants.WEBSITE_PATH, cssPathOriginal])
        self.cssHref = self.cssPathCopy.split(constants.WEBSITE_PATH)[-1]
        self.lang = lang
        self.categories = []

    def addCategory(self, category):
        self.categories.append(category)
        return self

    def addCategories(self, categories):
        self.categories += categories
        return self

    def addElement(self, contentBuilder, elementStack, newElement):
        if elementStack:
            targetForElement = elementStack[-1]
            targetStr = f"{targetForElement.__repr__()}"
        else:
            targetForElement = contentBuilder
            targetStr = f"contentBuilder"
        logging.debug(f"adding element: {newElement.__repr__()}; target is: {targetStr}")
        targetForElement << newElement

    def pageToHtml(self, page, category):
        logging.debug("generating HTML from Page Object")
        contentBuilder = ContentBuilder()
        elementStack = []
        previousElement = None
        queuedPop = False
        for adder in category.adders:
            # adder can be of an Adder class, or it could be a direction
            # first check if it is a direction, and if so, handle it as such
            if type(adder) is Adds.Direction:
                if queuedPop:
                    elementStack.pop()
                    queuedPop = False

                if adder == Adds.Direction.IN:
                    if previousElement is not None:
                        elementStack.append(previousElement)
                        previousElement = None
                elif adder == Adds.Direction.OUT:
                    if len(elementStack) > 1:
                        queuedPop = True
                else:
                    logging.warning(f"unknown direction: {adder}")
                continue
            # if we reach here, then adder is not a direction, and should be handled
            # as an adder

            if previousElement is not None:
                self.addElement(contentBuilder, elementStack, previousElement)

            if queuedPop:
                stackedElement = elementStack.pop()
                self.addElement(contentBuilder, elementStack, stackedElement)
                queuedPop = False

            previousElement = adder.add(page, self, category)

        if previousElement is not None:
            self.addElement(contentBuilder, elementStack, previousElement)
        if queuedPop:
            stackedElement = elementStack.pop()
            self.addElement(contentBuilder, elementStack, stackedElement)
            queuedPop = False

        while elementStack:
            stackedElement = elementStack.pop()
            self.addElement(contentBuilder, elementStack, stackedElement)

        return str(contentBuilder)

    def build(self):
        shutil.copyfile(self.cssPathOriginal, self.cssPathCopy)
        for category in self.categories:
            for page in category.pages:
                absoluteOutputFile = "/".join([constants.WEBSITE_PATH, page.getRelativeOutputFile(category)])
                open(absoluteOutputFile, 'w').write(self.pageToHtml(page, category))
