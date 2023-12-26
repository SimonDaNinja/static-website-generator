from . import constants
import os
import logging
import shutil
from . import Adds
from .ContentBuilder import HtmlElement, ContentBuilder
import logging

class WebsiteBuilder:

    def __init__(self, cssPathOriginal, lang, fullTitle, briefTitle, domainName, description, symbolDict):
        self.cssPathOriginal = cssPathOriginal
        self.cssPathCopy = "/".join([constants.WEBSITE_PATH, cssPathOriginal])
        self.cssHref = self.cssPathCopy.split(constants.WEBSITE_PATH)[-1]
        self.lang = lang
        self.fullTitle = fullTitle
        self.briefTitle = briefTitle
        self.categories = []
        self.domainName = domainName
        self.description = description
        self.symbolDict = symbolDict
        self.symbolsDir = "/".join([constants.WEBSITE_PATH, "symbols"])

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
        logging.debug(f"generating HTML from Page Object for:\npage: {page.fullTitle}\n, category: {category.categoryName}")
        contentBuilder = ContentBuilder()
        elementStack = []
        previousElement = None
        queuedPop = False
        adders = page.adders if page.adders is not None else category.adders
        for adder in adders:
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

        outputStr = str(contentBuilder)
        for name, imagePath in self.symbolDict.items():
            linkText = f"<img src = \"{imagePath}\" class=\"icon\">"
            outputStr = outputStr.replace(f":{name}:", linkText)

        return outputStr

    def build(self):
        shutil.copyfile(self.cssPathOriginal, self.cssPathCopy)
        if not os.path.exists(self.symbolsDir):
            os.makedirs(self.symbolsDir)
            for name, imagePath in self.symbolDict.items():
                extension = imagePath.split('.')[-1]
                newFile = "/".join([self.symbolsDir, f"{name}.{extension}"])
                shutil.copyfile(imagePath, newFile)
                self.symbolDict[name] = f"/symbols/{name}.{extension}"
        for category in self.categories:
            absoluteOutputDir = "/".join([constants.WEBSITE_PATH, category.relativeOutputDir])
            if not os.path.exists(absoluteOutputDir):
                os.makedirs(absoluteOutputDir)
            for page in category.pages:
                absoluteOutputFile = "/".join([constants.WEBSITE_PATH, page.getRelativeOutputFile(category)])
                open(absoluteOutputFile, 'w').write(self.pageToHtml(page, category))
