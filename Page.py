import urllib.parse
class Page:
    def __init__(self, fullTitle, briefTitle, description, fileName, bodyfile=None):
        self.fullTitle = fullTitle
        self.briefTitle = briefTitle
        self.description = description
        self.fileName = fileName
        self.bodyfile = bodyfile

    def getRelativeOutputFile(self, category):
        return "/".join([category.relativeOutputDir, self.fileName]) if category is not None else self.fileName

    def getUrl(self, category):
        url = urllib.parse.quote(self.getRelativeOutputFile(category))
        if url[0] != "/":
            url = "/" + url
        return url

class CategoryPage(Page):
    def __init__(self, category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category
        assert category.categoryPage is None, "category an not have more than one category page"
        category.categoryPage = self
