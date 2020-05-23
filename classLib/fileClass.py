import os
import time
import utils.converter as converter

class baseClass:
    def __init__(self, filepath, tag=""):
        self.filepath = filepath
        self.file = os.path.basename(filepath)
        self.filename = self.file.split(".")[0]
        self.path = filepath.replace(self.filename, "")
        self.tag = tag
        self.createTime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def showAttr(self):
        for item in self.__dict__.items():
            print("%s: %s"%(item[0], item[1]))

    def getAttr(self):
        attr_list = [ [item[0], item[1]] for item in self.__dict__.items()]
        return attr_list

    def to_corpus(self):
        corpus = converter.to_corpus(self)
        return corpus

class sx01(baseClass):
    def __init__(self, filepath, tag=""):
        baseClass.__init__(self, filepath, tag)
        self.showAttr()


class xl01(baseClass):
    def __init__(self, filepath, tag="", col='A'):
        baseClass.__init__(self, filepath, tag)
        self.col = col


class xl02(baseClass):
    def __init__(self, filepath, tag="", col='A'):
        baseClass.__init__(self, filepath, tag)
        self.col = col