import re

def tq_split(sentence, quote_start, quote_stop, split_symbol):
    words = []
    temp = ""
    for index, char in enumerate(sentence):
        temp += char
        if index == len(sentence) - 1 or sentence[index + 1] in quote_start or (sentence[index] in quote_stop + split_symbol and sentence[index + 1] not in quote_stop + split_symbol):
            words.append(temp)
            temp = ""
    return words

def tqSeg_(source):
    quote_start = ["(", "（", "【", "[", "《", "{"]
    quote_start_re = "[\(（【\[《{]"
    quote_stop =  [")", "）", "】", "]", "》", "}"]
    quote_stop_re =  "[\)）】\]》}]"
    #split_symbol = [",", "，", "：", " ", "·", "、", "。", "？", "-", "\n", ":", "*", "#m", "……", "#r"]
    split_symbol = [",", "，", "：", " ", "·", "、", "。", "？", "-", "\n", ":", "*", "#m", "……", "-"]
    split_symbol_re = u"[,，：\s·、。？:]"
    threshold = 3

    # Segmentation by symbol and quote
    dictionary_word = []
    dictionary_freq = []
    source_break = []
    for item in source:
        item = str(item)
        words = tq_split(item, quote_start, quote_stop, split_symbol)
        source_break.append(words)

    # Calculate segment frequancy
    for words in source_break:
        for word in words:
            if word not in dictionary_word:
                if len(re.findall(u"[\u4E00-\u9FA5]", word)) > 0 and len(word) >= threshold:
                    dictionary_word.append(word)
                    dictionary_freq.append(1)
                else:
                    dictionary_word.append(word)
                    dictionary_freq.append(0)
            else:
                if len(re.findall(u"[\u4E00-\u9FA5]", word)) > 0 and len(word) >= threshold:
                    dictionary_freq[dictionary_word.index(word)] += 1

    # Create stop position table
    spos_table = []
    freq_table = []
    for s_index, words in enumerate(source_break):
            freq_table.append([ dictionary_freq[dictionary_word.index(word)] for word in words ])
            if len(words) > 0:
                spos_list = [len(words[0])-1]
                for i in range(1, len(words)):
                    spos_list.append(spos_list[-1] + len(words[i]))
            else:
                spos_list = [0]
            spos_table.append(spos_list)

    # Create after segmentation word lists
    words_list = []
    real_dict_source = []
    real_dict_word = []
    for s_index, words in enumerate(source_break):
        words_temp = []
        source_str = str(source[s_index])
        spos_list = spos_table[s_index]
        freq_list = freq_table[s_index]
        word_list = words

        # Delete stop position
        del_time = 0
        freq_list_lenght = len(freq_list)
        for f_index, f_item in enumerate(freq_list):
            if f_index != freq_list_lenght - 1 and (freq_list[f_index] in [0,1] and freq_list[f_index + 1] in [0,1]):
                del spos_list[f_index - del_time]
                del_time += 1

        # Segmentation words by stop position list
        spos_last = 0
        for spos_cur in spos_list:
            spos_cur += 1
            if len(source_str[spos_last:spos_cur]) > 0 and len(re.findall(split_symbol_re ,source_str[spos_last:spos_cur][0])) != 0:
                str_cur = source_str[spos_last:spos_cur][1:]
            else:
                str_cur = source_str[spos_last:spos_cur]
            words_temp.append(str_cur)
            spos_last = spos_cur
        words_list.append(words_temp)
    return words_list

def tqSeg(source, threshold = 3):
    re_stopSym = r"[,.!?:;～\|、，。！？：；～~ ]"
    re_CNsym = r"[^\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5]"
    '''
    Quete Matcher
        Failure Mode:
            1. 【头饰-S3级(真品)】: '(真品)'
    '''
    re_OQuete = r"(?:\[|\(|\<|【|（|《|\{\「)"
    re_CQuete = r"(?:\]|\)|\>|】|）|》|\}\」)"
    re_Quete = r"(?:%s.+?%s)+?" % (re_OQuete, re_CQuete)
    '''
    CNSeg Matcher
        Failure Mode:
            1. 【
    '''
    re_CNSeg = r"[\u4E00-\u9FA5…\-_0-9a-zA-Z]+"
    re_stopSymbal = r"[\u4E00-\u9FA5…\-_0-9a-zA-Z＋－]+(?:[^\u4E00-\u9FA5…\-_0-9a-zA-Z]|$)"
    re_stopSymbal = r"[\u4E00-\u9FA5…\-_a-zA-Z＋－]+(?:[^\u4E00-\u9FA5…\-_a-zA-Z]|$)"

    #Extact CNSeg and quote by regular expression
    word_list = []
    for item in source:
        item = str(item).replace("\\n", ",")

        quote_list = re.findall(re_Quete, item)
        for q in quote_list:
            item = item.replace(q, ",")
        #quote_list = [ q for q in quote_list if len(re.findall(r"[\u4E00-\u9FA5]", q)) > 0]
        CNSeg_list = re.findall(re_stopSymbal, item)
        #print(item, "|", quote_list)
        word_list += CNSeg_list + quote_list + [None]

    #Create dictionary
    test_word_list = []
    new_word_list = []
    sentence_seg = []
    for seg in word_list:
        if seg == None:
            #freq_list = [ word_list.count(s_seg) for s_seg in sentence_seg]
            freq_list = []
            for s_seg in sentence_seg:
                if len(s_seg) <= threshold:
                    freq_list.append(1)
                else:
                    freq_list.append(word_list.count(s_seg))

            len_list = [ len(s_seg) for s_seg in sentence_seg]

            if sum(freq_list) == len(freq_list):
                new_word_list.append("".join(sentence_seg))
                test_temp = "".join(sentence_seg) ##
            else:
                new_sentence_seg = []
                temp_sentence = ""
                for ind, item in enumerate(zip(sentence_seg, freq_list)):
                    s, f = item
                    if f != 1:
                        if temp_sentence != "":
                            new_sentence_seg.append(temp_sentence)
                        new_sentence_seg.append(s)
                        temp_sentence = ""
                    else:
                        temp_sentence += s
                if temp_sentence != "":
                    new_sentence_seg.append(temp_sentence)
                new_word_list += new_sentence_seg

                test_temp = new_sentence_seg ##
            test_word_list.append([test_temp, str(freq_list)]) ##
            sentence_seg = []
        else:
            sentence_seg.append(seg)

    final_word_list = []
    for item in new_word_list:
        if len(item) > 0 and len(re.findall(r"[0-9]|" + re_stopSym, str(item[-1]))) > 0:
            item = item[:-1]
        if len(re.findall(r"[\u4E00-\u9FA5]", item)) > 0 and item not in final_word_list:
            final_word_list.append(item)

    return final_word_list

''''
from expy import getColumn
from datetime import datetime

manual_testset = ["[12463][3级S太阳帽子-精品][5017;5019][afsa]{是撒开飞机}【头饰-S3级(真品)】爱子：没有，我，我怎么可能会做那种事情呢……你，和朋s友E玩的4还开心吗？", "唔，1个人冒险固然很好，But只有我的陪伴，你也觉得会dwe21131aa孤单的呀~为了实力和财富，找到伙หกด伴向着冒险出发吧！"]

source = getColumn("testFile/WW翻译需求200117.docx.xlsx", column = 'A', sheet = 1, mode=1)[:1000]
source = manual_testset + source
#test_list = ["[12463][3级S太阳帽子-精品][5017;5019]爱子：没有，我，我怎么可能会做那种事情呢……你，和朋s友E玩的4还开心吗？","[2302][5012,2014;5012,2014]路明非：啊，炼金武器！这是学院炼金部的精品！新生，你赚大了！<% _G.tasksound(1162) %>"]
#res = tqSeg(source)
#for s in source:
#    print([s],"|", tqSeg2([s]),  tqSeg_([s]))

res = tqSeg_(source)
for s, t in zip(source, res[1]):
    print(s, "|", t)

start = datetime.now()

n = len(source)
new_list = tqSeg_(source)

end = datetime.now()
print(float((end-start).microseconds/n))

"""
Feature to add:
    ~1. Put back if no repeat-seg
    reconsider: 2. Not cut when seg len below threshold 
    3. Check quote-related sentence: new feature
    4. Improve efficiency if possible
"""
'''''