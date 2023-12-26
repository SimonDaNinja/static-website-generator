import urllib.parse
import datetime
import time
import re
from email.utils import formatdate

class Page:
    def __init__(self, fullTitle, briefTitle, description, fileName, bodyfile=None, adders = None):
        self.fullTitle = fullTitle
        self.briefTitle = briefTitle
        self.description = description
        self.fileName = fileName
        self.bodyfile = bodyfile
        self.adders = adders

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
        assert category.categoryPage is None, "category can not have more than one category page"
        category.categoryPage = self

class RssAblePage(Page):
    def __init__(self, date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = date

class BlogPage(RssAblePage):
    def __init__(self, bodyfile):
        regex = "(\d{4})-(\d{2})-(\d{2}): (.*).html"
        x = re.search(regex, bodyfile)
        assert x, f"incorrecly formated blog bodyfile name: \"{bodyfile}\""

        date = (int(x.group(1)), int(x.group(2)), int(x.group(3)))
        fullTitle = bodyfile[:-5]
        briefTitle = fullTitle
        contents = open(bodyfile, 'r').read()

        maxDescriptionLength = min(160, len(contents))
        maxDescription = contents[:maxDescriptionLength]
        lastIndex = maxDescription.rindex(" ")

        description = maxDescription[:lastIndex]
        super().__init__(date = date, fullTitle = fullTitle, briefTitle = briefTitle,
                         description = description, fileName = bodyfile, bodyfile = bodyfile)

class RssPage(Page):
    def __init__(self, categories, *args, **kwargs):
        self.itemIndex = 0
        self.categories = categories
        super().__init__(*args, **kwargs)

    def getItems(self):
        items = []
        for category in self.categories:
            pages = category.pages

            for page in pages:
                if not isinstance(page, RssAblePage):
                    continue
                items.append(RssItem(page))

        items.sort(key = lambda x : datetime.datetime(x.getYear(), x.getMonth(), x.getDay()))
        return items

    def getNextItem(self):
        items = self.getItems()
        if len(items) < self.itemIndex+1:
            return None
        item = self.getItems()[self.itemIndex]
        self.itemIndex += 1
        return item

    def resetItemIndex(self):
        self.itemIndex = 0

class RssItem:
    def __init__(self, rssAblePage):
        self.year, self.month, self.day = rssAblePage.date
        if rssAblePage.bodyfile is not None:
            self.description = open(rssAblePage.bodyfile, 'r').read()
        else:
            self.description = rssAblePage.description
        self.title = rssAblePage.fullTitle
        self.link = rssAblePage.fileName
        self.guid = f"{self.getYear()}-{self.getMonth()}-{self.getDay()}: {self.getTitle()}"
        return

    def getYear(self):
        return self.year

    def getMonth(self):
        return self.month

    def getDay(self):
        return self.day

    def setYear(self, year):
        self.year = year

    def setMonth(self, month):
        self.month = month

    def setDay(self, day):
        self.day = day

    def getPubDate(self):
        date = [self.getYear(), self.getMonth(), self.getDay()]
        return formatdate(time.mktime(datetime.datetime(*date).timetuple()), True)

    def getGuid(self):
        return self.guid

    def getLink(self):
        return self.link

    def getDescription(self):
        return self.description

    def getTitle(self):
        return self.title
