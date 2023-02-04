INDENTATION_WIDTH = 4

class HtmlString:
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
            if '\n' in other:
                lines = other.split('\n')
                for line in lines:
                    self << line
                return self
            while other and other[0] == " ":
                other = other[1:]
            if (len(other)+self.indentation) > self.maxWidth:
                spaces = [i for i, letter in enumerate(other) if letter==" "]
                cutIndex = 0
                for i in spaces:
                    if i+self.indentation < self.maxWidth:
                        cutIndex = i
                    else:
                        break
                if cutIndex == 0:
                    self.string += other
                    return self
                firstString = other[0:cutIndex]
                secondString = other[(cutIndex+1):]
                self << firstString
                self << secondString
                return self
            if self.string:
                self.string += "\n"
            self.string += " "*self.indentation
            self.string += other

        elif type(other) is HtmlElement:
            tagString = f"<{other.name}"
            if other.properties is not None:
                for prop, value in other.properties.items():
                    tagString += f" {prop}={value}"
                    addSpace = True
            if other.selfClosing:
                tagString += "/"
            tagString += ">"
            self << tagString
            if other.contents:
                if other.indent:
                    self << INDENTATION_WIDTH
                for content in other.contents:
                    self << content
                if other.indent:
                    self << -INDENTATION_WIDTH
                self << f"</{other.name}>"

        else:
            raise TypeError
        return self

class HtmlElement:
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
