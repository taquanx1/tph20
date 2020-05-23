# CTSL.CHULA

"""
file format: .tqgloss
data format: [<source>, <target>, <comment>]

"""
import time
import pickle
from utils.expy import saveData
from utils.tqSeg import tqSeg
from utils.expy import getColumn

class gloss:
    '''

    Working process:
     1.
    '''
    def __init__(self, gloss_path = None, gloss_name="" ,gloss_list=None, gloss=None):
        self.gloss_path = gloss_path
        self.gloss_name = gloss_name
        self.source_gloss_list = []
        self.trans_gloss_list = []
        self.gloss = gloss if gloss != None else []
        self.createTime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        if gloss_path != None:
            self.load_file()

    def load_file(self):
        '''
        To break sentence and replace by gloss
        :step:
            0. duplicate ori_gloss_list, then use in following process
            1. break sentence into sub-sentence by tqseg()
            2. replace by gloss
            3. asign sub-sentence to source_gloss_list or trans_gloss_list

        :return: Null
        '''
        self.trans_gloss_list = getColumn(self.gloss_path, column='B', sheet=1, mode=1)
        temp_source = []
        temp_trans = []
        for s_index, s in enumerate(getColumn(self.gloss_path, column='A', sheet=1, mode=1)):
            if len(s) > 0:
                temp_source.append(s)
                temp_trans.append(self.trans_gloss_list[s_index])
        self.source_gloss_list = temp_source
        self.trans_gloss_list = temp_trans

        #self.source_gloss_list = [ item for item in getColumn(self.gloss_path, column='A', sheet=1, mode=1) if len(item) > 3]
        #self.trans_gloss_list = [ item for item in getColumn(self.gloss_path, column='B', sheet=1, mode=1) if len(item) > 3]


    def add_gloss(self, new_gloss):
        '''
        To add new gloss to gloss and preprocess
        :param new_gloss:
        :return:
        '''
        self.gloss += new_gloss

    def __add__(self, other):
        self.source_gloss_list = self.source_gloss_list + other.source_gloss_list
        self.trans_gloss_list = self.trans_gloss_list + other.trans_gloss_list
        return self

    def export_to_xlsx(self):
        xlsx_data = [ [s, t] for s, t in zip(self.source_gloss_list, self.trans_gloss_list)]
        saveData("%s.xlsx"%self.gloss_name, xlsx_data)

    def sort(self):
        temp_gloss_list = [[c, t] for c, t in zip(self.source_gloss_list, self.trans_gloss_list)]
        temp_gloss_list = sorted(temp_gloss_list, key=lambda x: len(x[0]), reverse=True)
        temp_gloss_list = zip(*temp_gloss_list)
        temp_gloss_list = list(map(list, temp_gloss_list))
        self.source_gloss_list = temp_gloss_list[0]
        self.trans_gloss_list = temp_gloss_list[1]

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