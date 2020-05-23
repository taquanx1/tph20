import jieba
import jieba.posseg as pseg
import os
import expy as expy
#from .expy import getData
from datetime import datetime
import pickle
import threading

class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

def remove_tail(string):
    tail_list = [',', ' ', '.', '!', '?', ':', ';', '~', '～', '\\', '|', '、', '，', '。', '！', '？', '：', '；']
    new_string = string if string[-1] not in tail_list else string[:-1]

    return new_string

def token_freq(gloss_data):
    gloss_n = len(gloss_data)

    lexicon_list = []
    lexiconCount_list = []
    for gloss_index, item in enumerate(gloss_data):
        if gloss_index%1000 == 0 and gloss_index != 0:
            print("%d/%d"%(gloss_index, gloss_n))
        gloss_CN, gloss_TH = item[0], item[1]
        token_list = jieba.cut(str(gloss_CN), cut_all=True)
        for token in token_list:
            if token in lexicon_list:
                token_index = lexicon_list.index(token)
                cur_count = int(lexiconCount_list[token_index].split('\t')[-1])
                lexiconCount_list[token_index] = "%s\t%d"%(token, cur_count + 1)
            else:
                lexicon_list.append(token)
                lexiconCount_list.append("%s\t%d"%(token, 1))

    lexiconCount_list = sorted(lexiconCount_list, key= lambda x:int(x.split('\t')[-1]), reverse=True)
    lexiconCount_list_out = [ item.split('\t') for item in lexiconCount_list ]
    expy.saveData('./lexicon.xlsx', lexiconCount_list_out)

def row_occurance_multi(gloss_data_batch , gloss_data, threshold_len = 2):
    if type(gloss_data).__name__ == 'list':
        gloss_CN_list = [ str(row[0]) for row in gloss_data if len(str(row[0])) >= threshold_len]
        gloss_CN_str = "\n".join(gloss_CN_list)
    elif type(gloss_data).__name__ == 'str':
        gloss_CN_str = gloss_data

    occurance_list = []
    finished_CN_list = []
    for CN_index, CN_string in enumerate(gloss_data_batch):
        if CN_string not in finished_CN_list and len(CN_string) >= threshold_len:
            CN_string = remove_tail(CN_string)
            cur_count = gloss_CN_str.count(CN_string)
            POS = '\r'.join([ "%s\t%s"%(list(item)[0], list(item)[1]) for item in pseg.cut(CN_string,use_paddle=True) ])
            occurance_list.append([CN_string, str(POS), cur_count]) #float(cur_count/gloss_n)*100]
            finished_CN_list.append(CN_string)

    return occurance_list

def row_occurance(gloss_data, threshold_len = 2, filename = 'unknow'):
    '''
    To calculate and sort each row of gloss by number of occurances
    :param gloss_data: list of gloss data (source language) ex. [["冒险", "ผจญภัย" ...], ["冒险", "ผจญภัย" ...], ..., [...] ]
    :param threshold_len:
    :return:
    '''
    gloss_CN_list = [ str(row[0]) for row in gloss_data if len(str(row[0])) >= threshold_len]

    gloss_list = [ [str(row[0]), str(row[1])] for row in gloss_data if len(row) >= 2 and len(str(row[0])) >= threshold_len]
    '''
    gloss_list = []
    for row in gloss_data:
        if len(str(row[0])) >= threshold_len:
            print(row)
            gloss_list.append([str(row[0]), str(row[1])])
    '''

    gloss_CN_str = "\n".join(gloss_CN_list)
    gloss_n = len(gloss_CN_list)

    ss = datetime.now()
    occurance_list = []
    finished_CN_list = []
    for CN_index, item in enumerate(gloss_list):
        CN_string = item[0]
        if CN_string not in finished_CN_list and len(CN_string) >= threshold_len:
            CN_string = remove_tail(CN_string)
            cur_count = gloss_CN_str.count(CN_string)
            #POS = '\r'.join([ "%s\t%s"%(list(item)[0], list(item)[1]) for item in pseg.cut(CN_string,use_paddle=True) ])
            pos_signature = '-'.join([ str(list(item)[1]) for item in pseg.cut(CN_string,use_paddle=True) ])
            occurance_list.append([CN_string, item[1],str(pos_signature), cur_count]) #float(cur_count/gloss_n)*100]
            finished_CN_list.append(CN_string)

        if (CN_index % 5000 == 0 or CN_index == gloss_n - 1) and CN_index != 0:
            # occurance_list = sorted(occurance_list, key=lambda x: int(x.split('\t')[-1]), reverse=True)
            occurance_list = sorted(occurance_list, key=lambda x: int(x[3]), reverse=True)
            f = open('%s.tqgl'%filename, 'wb')
            pickle.dump(occurance_list, f)
            f.close()

            # expy.saveData('./lexicon.xlsx', [ item.split('\t') for item in occurance_list])
            expy.saveData('./%s.xlsx'%filename, occurance_list)

            ee = datetime.now()
            print(CN_index, ee - ss)
            ss = datetime.now()

    return occurance_list

def back_row_occurance(gloss_data, threshold_len = 2):
    '''
    To calculate and sort each row of gloss by number of occurances
    :param gloss_data: list of gloss data (source language) ex. [["冒险", "ผจญภัย" ...], ["冒险", "ผจญภัย" ...], ..., [...] ]
    :param threshold_len:
    :return:
    '''
    gloss_CN_list = [ str(row[0]) for row in gloss_data if len(str(row[0])) >= threshold_len]
    gloss_CN_str = "\n".join(gloss_CN_list)
    gloss_n = len(gloss_CN_list)

    ss = datetime.now()
    occurance_list = []
    finished_CN_list = []
    for CN_index, CN_string in enumerate(gloss_CN_list):
        if CN_string not in finished_CN_list and len(CN_string) >= threshold_len:
            CN_string = remove_tail(CN_string)
            cur_count = gloss_CN_str.count(CN_string)
            POS = '\r'.join([ "%s\t%s"%(list(item)[0], list(item)[1]) for item in pseg.cut(CN_string,use_paddle=True) ])
            occurance_list.append([CN_string, str(POS), cur_count]) #float(cur_count/gloss_n)*100]
            finished_CN_list.append(CN_string)

        if (CN_index % 5000 == 0 or CN_index == gloss_n - 1) and CN_index != 0:
            # occurance_list = sorted(occurance_list, key=lambda x: int(x.split('\t')[-1]), reverse=True)
            occurance_list = sorted(occurance_list, key=lambda x: int(x[2]), reverse=True)
            f = open('RO_row_occurance.tqgl', 'wb')
            pickle.dump(occurance_list, f)
            f.close()

            # expy.saveData('./lexicon.xlsx', [ item.split('\t') for item in occurance_list])
            expy.saveData('./RO_row_occurance.xlsx', occurance_list)

            ee = datetime.now()
            print(CN_index, ee - ss)
            ss = datetime.now()

def read_xlsx(xlsx_path):
    glossLib_path = xlsx_path
    gloss_data = expy.getData(glossLib_path)
    gloss_n = len(gloss_data)
    xlsx_name = xlsx_path.split('/')[-1].split('.')[0]

    f = open('%s.tqtf'%xlsx_name, 'wb')
    pickle.dump(gloss_data, f)
    f.close()

    return '%s.tqtf'%xlsx_name

def load_tqtf(tqtf_path):
    f = open(tqtf_path, 'rb')
    gloss_data = pickle.load(f)
    f.close()
    print("*tqtf loaded!")
    return gloss_data

def row_occurance_multi_execute(gloss_data, batch_n = 5000):
    gloss_CN_list = [str(row[0]) for row in gloss_data if len(str(row[0])) >= 2]
    gloss_CN_str = "\n".join(gloss_CN_list)

    gloss_batch = []
    for i in range(len(gloss_CN_list) // batch_n + 1):
        cur_batch = gloss_CN_list[i * batch_n: (i * batch_n) + batch_n]
        gloss_batch.append(cur_batch)

    result = []
    threads = []
    for index, cur_batch in enumerate(gloss_batch):
        t = MyThread(row_occurance_multi, args=(cur_batch, gloss_CN_str, 2,))
        threads.append(t)
    print(len(threads))
    for i, t in enumerate(threads):
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
        result += t.get_result()

    occurance_list = sorted(result, key=lambda x: int(x[2]), reverse=True)
    f = open('RO_row_occurance_multi.tqgl', 'wb')
    pickle.dump(occurance_list, f)
    f.close()

    # expy.saveData('./lexicon.xlsx', [ item.split('\t') for item in occurance_list])
    expy.saveData('./RO_row_occurance_multi.xlsx', occurance_list)
    # row_occurance(gloss_data)

def pos_match_point(target_pos_list, string_pos):
    import re
    for target_pos in target_pos_list:
        #target_pos.replace("?", "[a-z]")
        re_match = re.match(target_pos, string_pos)
        if re_match!= None and re_match.span() == (0, len(string_pos)):
            return 1
    return 0

def row_occurance_filter(xlsx_path = None, stop_word_path = None, freq_threshold = 1, filename = "unknow", occurance_list = None):
    POS_pattern = [
        ['', ''],
        ['', ''],
        ['', ''],
        ['', ''],
        ['', ''],
        ['', ''],
        ['', '']
    ]
    POS_match = ['n', 'vn']
    target_pos = ["n", "n[a-z]+", "n[a-z]*(?:-n[a-z]*)",'v[a-z]+', "v[a-z]*(?:-n[a-z]*)", "b-n[a-z]+"]

    if occurance_list == None and xlsx_path == None:
        print('Error: xlsx_path and occurance_list are ‘None’')
        return -1
    elif occurance_list != None:
        rowO_data = occurance_list
    elif xlsx_path != None:
        rowO_data = expy.getData(xlsx_path)

    finish_row = []
    new_gloss = []
    for cur_rowO in rowO_data:
        if pos_match_point(target_pos, cur_rowO[2] ) >= 1 and\
            int(cur_rowO[3]) >= freq_threshold and\
            len(cur_rowO[0]) >= 2 and\
            str(cur_rowO[0]) not in finish_row:
            print(cur_rowO[0], type(cur_rowO[0]))
            new_gloss.append(cur_rowO)
            finish_row.append(str(cur_rowO[0]))
    if stop_word_path != None:
        stop_word = expy.getData(stop_word_path)
        stop_word = [ str(item) for item in stop_word]
        new_gloss = [ item for item in new_gloss if str(item[0]) not in stop_word]


    expy.saveData('./%s.xlsx'%filename, new_gloss)

def gloss_from_translated(translate_path, threshold_len = 2):
    if translate_path.split('.')[-1] == 'xlsx':
        tqtf_filename = read_xlsx(translate_path)
    elif translate_path.split('.')[-1] == 'tqtf':
        tqtf_filename = translate_path
    else:
        print("Error in gloss_from_translated: not support file *.%s"%translate_path.split('.')[-1])
        return -1
    gloss_data = load_tqtf(tqtf_filename)
    occurance_list = row_occurance(gloss_data, threshold_len, filename = tqtf_filename)
    row_occurance_filter(freq_threshold = 10, occurance_list = occurance_list)

def merge_gloss(gloss1_path, gloss2_path):
    gloss1_name = gloss1_path.split('/')[-1].split('.')[0]
    gloss2_name = gloss2_path.split('/')[-1].split('.')[0]

    gloss1_data = expy.getData(gloss1_path)
    gloss2_data = expy.getData(gloss2_path)
    merged_data = gloss1_data + gloss2_data
    merged_data_sorted = sorted(merged_data, key=lambda x:len(x[0]), reverse = True)

    merged_data_sorted_killRepeat = []
    existed = []
    for item in merged_data_sorted:
        CN = str(item[0])
        if CN not in existed:
            merged_data_sorted_killRepeat.append(item)
            existed.append(CN)

    expy.saveData('%s_%s_merge_gloss.xlsx'%(gloss1_name, gloss2_name), merged_data_sorted_killRepeat)

start = datetime.now()


#tqgl_path = 'RO_glossLib.tqgl'
#gloss_data = load_tqgl(tqgl_path)

#row_occurance_filter('./RO_row_occurance_multi.xlsx', 4)

gloss_from_translated('./RO_row_occurance_multi.xlsx')

end = datetime.now()
print(end - start)