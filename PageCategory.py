class PageCategory:

    def __init__(self, categoryName, pages = None, relativeOutputDir = None, adders = None,
                 superCategory = None):
        self.categoryPage = None
        self.superCategory = superCategory
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
        if superCategory is not None:
            self.relativeOutputDir = "/".join([superCategory.relativeOutputDir, self.relativeOutputDir])

    def addPage(self, page):
        self.pages.append(page)

    def addPages(self, pages):
        self.pages += pages

    def addAdder(self, adder):
        self.adders.append(adder)

    def addAdders(self, adders):
        self.adders += adders
