import pickle
import re
from .expy import getColumn
from classLib.corpus import corpus
import os

def sx01_to_corpus(filepath):
    """
    Dump tqxliff as a class
    :param filepath:
    :return:
    """
    file = os.path.basename(filepath)
    filename = file.split(".")[0]

    f = open(filepath, 'r', encoding='utf-8')
    lines = f.readlines()[-1]
    f.close()

    re_unit = r'<trans-unit id="[0-9a-z-]+".*?<\/trans-unit>'
    ori_unit_list = re.findall(re_unit, lines)

    re_source = r'<source><g id="[0-9]+">(.*?)</g></source>'
    re_seg_source = r'<seg-source>(.*)</seg-source>'
    re_seg_source_mrk = r'<mrk mtype="seg" mid="[0-9]+">(.*?)</mrk>'
    re_seg_source_g = r'<g id="[0-9]+">(.*?)</g>'
    re_seg_source_x = r'<x id="[0-9]+">(.*?)</x>'
    #re_target = r'<target><g id="[0-9]+"><mrk mtype="seg" mid="[0-9]+">(.*?)</mrk></g></target>'
    re_target = r'<target>(.*?)</target>'
    re_target_mrk = r'<mrk mtype="seg" mid="[0-9]+">(.*?)</mrk>'
    re_sdl = r'<sdl:seg id="[0-9]+" (.*?)>'
    re_sdl_seg = r'<sdl:seg id="([0-9]+)" (.*?)>'

    source_target_list = []
    source_target_status_list = []
    for ind, unit in enumerate(ori_unit_list):
        source = re.findall(re_source, unit)
        seg_source = re.findall(re_seg_source, unit)
        seg_source_mrk = re.findall(re_seg_source_mrk, seg_source[0])
        target = re.findall(re_target, unit)
        target_mrk = re.findall(re_target_mrk, target[0]) if target != [] else []
        sdl = re.findall(re_sdl, unit)

        if len(seg_source_mrk) > 1:
            re_mid = r'<mrk mtype="seg" mid="([0-9]+?)">(.*?)</mrk>'
            mid_list = [ int(item[0]) for item in re.findall(re_mid, seg_source[0])]
            mid_list_n = len(mid_list)
            mid_dif = sorted(mid_list, key= lambda x:x)[0]

            source_find = [ item for item in re.findall(re_mid, seg_source[0])]
            target_find = [ item for item in re.findall(re_mid, target[0])]
            sdlSta_find = [ item for item in re.findall(re_sdl_seg, unit)]
            source_mid_list = list(list(zip(*source_find))[0]) if source_find != [] else []
            target_mid_list = list(list(zip(*target_find))[0]) if target_find != [] else []
            sdlSta_mid_list = list(list(zip(*sdlSta_find))[0]) if sdlSta_find != [] else []
            for i in range(mid_list_n):
                temp_source = source_find[i][1] if i + mid_dif in source_mid_list else ""
                temp_target = target_find[i][1] if i + mid_dif in target_mid_list else ""
                temp_sdlSta = sdlSta_find[i][1] if i + mid_dif in sdlSta_mid_list else ""

                source_target_status_list.append([temp_source, temp_target, temp_sdlSta])
        else:
            temp_source = seg_source_mrk[0] if seg_source_mrk!= [] else re.findall(re_seg_source_g, seg_source[0])[0] if re.findall(re_seg_source_g, seg_source[0]) != [] else re.findall(re_seg_source_x, seg_source[0])[0] if re.findall(re_seg_source_x, seg_source[0])!=[] else ""
            temp_target = target_mrk[0] if target_mrk != [] else ""
            temp_sdlSta = sdl[0] if sdl != [] else ""

            source_target_status_list.append([temp_source, temp_target, temp_sdlSta])

    new_corpus = corpus(filename, source_target_status_list)
    return new_corpus

def xl01_to_corpus(filepath, col):
    file = os.path.basename(filepath)
    filename = file.split(".")[0]
    source = getColumn(filepath, column=col, sheet=1, mode=1)
    corpus_list = [ [s, "", ""] for s in source]
    new_corpus = corpus(filename, corpus_list)
    return new_corpus

def xl02_to_corpus(filepath):
    file = os.path.basename(filepath)
    filename = file.split(".")[0]
    source = getColumn(filepath, column='A', sheet=1, mode=0)
    target = getColumn(filepath, column='B', sheet=1, mode=0)
    corpus_list = [ [s, t, ""]  for s, t in zip(source, target) if s == t]
    new_corpus = corpus(filename, corpus_list)
    return new_corpus

def to_corpus(object):
    if type(object).__name__ == "sx01":
        new_corpus = sx01_to_corpus(object.filepath)
    elif type(object).__name__ == "xl01":
        new_corpus = xl01_to_corpus(object.filepath, object.col)
    elif type(object).__name__ == "xl02":
        new_corpus = xl02_to_corpus(object.filepath)
    else:
        new_corpus = corpus()

    return new_corpus
