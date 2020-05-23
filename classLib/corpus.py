"""
file format: .tqcorpus
data format: [<source>, <target>, <comment>]

"""
import time
import pickle
from utils.expy import saveData, getData
from utils.tqSeg import tqSeg
import classLib.gloss as gs

class corpus:
    '''

    Working process:
     1.
    '''
    def __init__(self, corpus_name="", corpus_list=None, gloss=None, threshold = 3):
        self.corpus_name = corpus_name
        self.ori_corpus_list = corpus_list if corpus_list != None else []
        self.source_corpus_list = None
        self.trans_corpus_list = None
        self.gloss = gloss if gloss != None else gs.gloss()
        self.createTime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.threshold = threshold

        #self.add_gloss(self.gloss)
        self.preprocess()
        self.dumpCorpus()

    def preprocess(self, report = False):
        '''
        To break sentence and replace by gloss
        :step:
            0. duplicate ori_corpus_list, then use in following process
            1. break sentence into sub-sentence by tqseg()
            2. replace by gloss
            3. asign sub-sentence to source_corpus_list or trans_corpus_list

        :return: Null
        '''
        from datetime import datetime
        import re

        start = datetime.now()
        #temp_list = [ item[0][0] for item in self.ori_corpus_list]
        temp_list = [item[0] for item in self.ori_corpus_list]
        ori_str = "".join(temp_list)
        self.source_corpus_list = tqSeg(temp_list, threshold = self.threshold)
        self.trans_corpus_list = [ "" for item in self.source_corpus_list ]

        #Glossy replacement
        new_source_corpus_list = []
        if len(self.gloss.source_gloss_list) != 0:
            self.gloss.sort()
            for c_index, c in enumerate(self.source_corpus_list):
                if len(c) >= self.threshold:
                    for g_index, g in enumerate(self.gloss.source_gloss_list):
                        c = c.replace(g, self.gloss.trans_gloss_list[g_index])
                    new_source_corpus_list.append(c)
            self.source_corpus_list = new_source_corpus_list

        corpus_str = "".join(self.source_corpus_list)
        ori_n = len(re.findall(r'[\u4E00-\u9FA5]', ori_str))
        corpus_n = len(re.findall(r'[\u4E00-\u9FA5]', corpus_str))
        end = datetime.now()

        print("Preprocessing finish!\nRemaining: %f%s (%d/%d)\nUsing: %fs"
              %(float(corpus_n/ori_n)*100, '%', corpus_n, ori_n, float(str((end-start).microseconds))/1000000))


    def add_gloss(self, new_gloss):
        '''
        To add new gloss to corpus and preprocess
        :param new_gloss:
        :return:
        '''
        self.gloss += new_gloss
        self.preprocess()

    def __add__(self, other):
        new_corpus_list = self.ori_corpus_list + other.ori_corpus_list
        new_corpus = corpus(self.corpus_name, new_corpus_list)
        return new_corpus

    def export_to_xlsx(self, xlsx_name = "corpus_%s.xlsx"):
        xlsx_data = [ [s, t] for s, t in zip(self.source_corpus_list, self.trans_corpus_list)]
        saveData(xlsx_name%self.corpus_name, xlsx_data)

    def dumpCorpus(self):
        if self.corpus_name != "":
            f = open("%s.tqcp"%self.corpus_name, 'wb')
            pickle._dump(self, f)
            f.close()

def load_corpus(corpus_filepath):
    f = open(corpus_filepath, 'rb')
    corpus = pickle.load(f)
    f.close()
    return corpus