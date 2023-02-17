import logging
from LocalLogger import logger

INDENTATION_WIDTH = 4

class ContentBuilder:
    def __init__(self, maxWidth=80):
        self.string = ""
        self.indentation = 0
        self.maxWidth = maxWidth

    def __str__(self):
        return self.string

    def __lshift__(self, other):
        if type(other) is int:
            self.indentation += other
        elif type(other) is str:
            self << StringElement(other)
        elif isinstance(other, ContentElement):
            other.addSelf(self)
        else:
            raise TypeError
        return self

class ContentElement:
    def __init__(self, addSelf = lambda builder : logger.warning(
    f"Default builder provided! Doing nothing!")):
        self.addSelf = addSelf

class StringElement(ContentElement):
    def __init__(self, string):
        self.string = string

    def addSelf(self, builder):
        if '\n' in self.string:
            lines = self.string.split('\n')
            for line in lines:
                builder << line
            return
        while self.string and self.string[0] == " ":
            self.string = self.string[1:]
        if (len(self.string)+builder.indentation) > builder.maxWidth:
            spaces = [i for i, letter in enumerate(self.string) if letter==" "]
            cutIndex = 0
            for i in spaces:
                if i+builder.indentation < builder.maxWidth:
                    cutIndex = i
                else:
                    break
            if cutIndex == 0:
                builder.string += self.string
                return
            firstString = self.string[0:cutIndex]
            secondString = self.string[(cutIndex+1):]
            builder << firstString
            builder << secondString
            return
        if builder.string:
            builder.string += "\n"
        builder.string += " "*builder.indentation
        builder.string += self.string

class HtmlElement(ContentElement):
    def __init__(self, name, contents = None, properties = None, indent = True, selfClosing = False):
        self.name = name
        if contents is None:
            self.contents = list()
        elif type(contents) is list:
            self.contents = contents
        else:
            self.contents = [contents]
        self.properties = properties
        self.indent = indent
        self.selfClosing = selfClosing

    def addSelf(self, builder):
        tagString = f"<{self.name}"
        if self.properties is not None:
            for prop, value in self.properties.items():
                tagString += f" {prop}={value}"
        if self.selfClosing:
            tagString += "/"
        tagString += ">"
        builder << tagString
        if self.contents:
            if self.indent:
                builder << INDENTATION_WIDTH
            for content in self.contents:
                if type(content) is str:
                    builder << content
                else:
                    builder << content
            if self.indent:
                builder << -INDENTATION_WIDTH
            builder << f"</{self.name}>"

    
    def __lshift__(self, other):
        if type(other) is dict:
            for key, val in other.items():
                self.properties[key] = value
        else:
            self.contents.append(other)
        return self

    def __str__(self):
        string = "{"
        string += f"name: {self.name}, "
        string += f"contents: {self.contents}, "
        string += f"properties: {self.properties}, "
        string += f"indent: {self.indent}, "
        string += f"selfClosing: {self.selfClosing} "
        string += "}"
        return string

    def __repr__(self):
        return str(self)
