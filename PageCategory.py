class PageCategory:

    def __init__(self, categoryName, pages = None, adders = None, relativeOutputDir = None):
        if pages is None:
            self.pages = list()
        else:
            self.pages = pages
        if adders is None:
            self.adders = list()
        else:
            self.adders = adders
        self.categoryName = categoryName
        if relativeOutputDir is None:
            self.relativeOutputDir = categoryName
        else:
            self.relativeOutputDir = relativeOutputDir

    def addPage(self, page):
        self.pages.append(page)

    def addPages(self, pages):
        self.pages += pages

    def addAdder(self, adder):
        self.adders.append(adder)

    def addAdders(self, adders):
        self.adders += adders

    def setPageAdders(self):
        for page in self.pages:
            page.adders = self.adders
