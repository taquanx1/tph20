# CTSL.CHULA

"""
file format: .tqgloss
data format: [<source>, <target>, <comment>]

"""
import time
import pickle
from utils.expy import saveData
from utils.tqSeg import tqSeg

class gloss:
    '''

    Working process:
     1.
    '''
    def __init__(self, gloss_name="", gloss_list=None, gloss=None):
        self.gloss_name = gloss_name
        self.source_gloss_list = None
        self.trans_gloss_list = None
        self.gloss = gloss if gloss != None else []
        self.createTime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        self.add_gloss(self.gloss)
        self.preprocess()
        self.dumpgloss()

    def preprocess(self):
        '''
        To break sentence and replace by gloss
        :step:
            0. duplicate ori_gloss_list, then use in following process
            1. break sentence into sub-sentence by tqseg()
            2. replace by gloss
            3. asign sub-sentence to source_gloss_list or trans_gloss_list

        :return: Null
        '''
        pass

    def add_gloss(self, new_gloss):
        '''
        To add new gloss to gloss and preprocess
        :param new_gloss:
        :return:
        '''
        self.gloss += new_gloss

    def __add__(self, other):
        self.ori_gloss_list + other.ori_gloss_list
        self.preprocess()

    def export_to_xlsx(self):
        xlsx_data = [ [s, t] for s, t in zip(self.source_gloss_list, self.trans_gloss_list)]
        saveData("%s.xlsx"%self.gloss_name, xlsx_data)

    def dumpgloss(self):
        if self.gloss_name != "":
            f = open("%s.tqcp"%self.gloss_name, 'wb')
            pickle._dump(self, f)
            f.close()

def load_gloss(gloss_filepath):
    f = open(gloss_filepath, 'rb')
    gloss = pickle.load(f)
    f.close()
    return gloss