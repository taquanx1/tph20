from utils.expy import getData, saveData, getColumn, getSheetlist
import os
import re
import pickle
from datetime import datetime
from utils.logTool import Print
import jieba

def get_colChar_from_sheetData(sheetData):
    '''
    Get colChar from sheet data
    :param sheetData:
    :return:

    Condition to process current sheet:
        1. sheet not empty or have more than 2 row: len(sheetData) >= 2
        2. sheet have more than 2 column: len(sheetData[0]) >= 2


    '''

def get_source_target(filepath):
    '''
    Find translated column pair and return as list
    :param filepath:
    :return:
    '''
    sheet_list = getSheetlist(filepath)

    allSheet_data_process = []
    for sheet_index, sheet in enumerate(sheet_list):
        cur_sheet_translated_data = getData(filepath, sheet_num = sheet_index)

        # if cur_sheet_translated_data not empty
        if cur_sheet_translated_data != []:
            cur_sheet_data_row_n = len(cur_sheet_translated_data)
            cur_sheet_data_firstCol_n = len(cur_sheet_translated_data[0])

            # this translated_data have to contain more than 1 row and 1 col
            if  cur_sheet_data_row_n >= 2 and cur_sheet_data_firstCol_n >= 2:


                # get the row that have same column number with first row and count
                gloss_col_list = []
                load_count = 0
                for col_index in range(cur_sheet_data_firstCol_n):
                    temp_col = []
                    for row in cur_sheet_translated_data:
                        if len(row) == cur_sheet_data_firstCol_n:
                            load_count += 1
                            temp_col.append(row[col_index])
                    gloss_col_list.append(temp_col)
                #print("[%d/%d] %s sheet: %s"%(load_count/cur_sheet_data_firstCol_n, cur_sheet_data_row_n, filepath, sheet))
                '''
                # get the row that have same column number with first row and count
                gloss_col_list = []
                load_count = 0
                for row in cur_sheet_translated_data:
                    temp_col = []
                    if row != []:
                        load_count += 1
                        temp_col.append(row)
                    gloss_col_list.append(temp_col)
                '''

                ## get CN/TH column number
                CN_col_count = [ len(re.findall(r"[\u4e00-\u9fa5]", "".join(map(str, col)))) for col in gloss_col_list]
                TH_col_count = [ len(re.findall(r"[\u0E00-\u0E7F]", "".join(map(str, col)))) for col in gloss_col_list]
                CN_max_index = CN_col_count.index(max(CN_col_count))
                TH_max_index = TH_col_count.index(max(TH_col_count))
                #print(CN_col_count)
                #print(TH_col_count)

                # get non-empty CN/TH sentences from each row
                sheet_data_process = []
                for row in cur_sheet_translated_data[1:]:
                    if len(row) >= CN_max_index + 1 and len(row) >= TH_max_index + 1:
                        cur_CN_sentence = row[CN_max_index]
                        cur_TH_sentence = row[TH_max_index]
                        if cur_CN_sentence != '' and cur_TH_sentence != '':
                            sheet_data_process.append([cur_CN_sentence, cur_TH_sentence, filepath, sheet])

                # add to allSheet_data_process
                allSheet_data_process += sheet_data_process
                print("[%d/%d] %s sheet: %s %d-%d" % (load_count / cur_sheet_data_firstCol_n, cur_sheet_data_row_n, filepath, sheet, CN_max_index, TH_max_index))
            else:
                Print("./log_glossFile_search.txt", "Error: sheet: '%s' in file: '%s' not enough column or row!" % (sheet, filepath))
        else:
            Print("./log_glossFile_search.txt", "Error: sheet: '%s' in file: '%s' is empty!"%(sheet, filepath))
    return allSheet_data_process

def gloss_filter(saved_CN, translated_data):
    '''
    
    :param saved_CN:
    :param cur_translated_data:
    :return:
    '''
    unrepeat_gloss = []
    for item in translated_data:
        CN_string = item[0]
        TH_string = item[1]
        if CN_string not in saved_CN and CN_string != '' and TH_string != '':
            unrepeat_gloss.append(item)
            saved_CN.append(CN_string)
    return unrepeat_gloss, saved_CN

def gloss_search(path):
    '''
    Search all translated file in <path> and save in .xlsx file
    :param path:
    :return:
    '''
    filepath_list = [ path + filename for filename in os.listdir(path) if filename.split('.')[-1] == 'xlsx' or filename.split('.')[-1] == 'xls']
    filepath_list_n = len(filepath_list)

    gloss_data = []
    saved_CN = []
    for file_index, filepath in enumerate(filepath_list):
        # Get CN/TH column by auto-search function "get_source_target"
        cur_gloss_data = get_source_target(filepath)

        # Get non-repeated row and
        unrepeat_row_list, saved_CN_update = gloss_filter(saved_CN, cur_gloss_data)
        print("--%s unrepeat: %d"%(str(filepath), len(unrepeat_row_list)))
        gloss_data += unrepeat_row_list
        saved_CN = saved_CN_update

        # Save every 10 files
        if (file_index != 0 and file_index%10 == 0) or file_index == filepath_list_n-1:
            time_now = datetime.now()
            filename = str(time_now)[:-5].replace(" ", "").replace(":", "").replace("-", "")
            print("-----(%d/%d)Save temp file-----"%(file_index, filepath_list_n))
            #save_filename = './%s.xlsx'%filename
            save_filename = './all_xlsx_search_translatePair.xlsx'
            saveData(save_filename, gloss_data)

def gloss_clean(path):
    gloss_data = getData(path)

    output_list = []
    for row in gloss_data:
        CN_col = str(row[0])
        TH_col = str(row[1])
        TH_in_CN_col = re.findall(r"[\u0E00-\u0E7F]+", CN_col)
        CN_in_TH_col = re.findall(r"[\u4e00-\u9fa5]+", TH_col)
        if TH_in_CN_col == [] and CN_in_TH_col == []:
            output_list.append(row)

    saveData("cleaned.xlsx", output_list)

def gloss_tokenize(path):
    gloss_data = getData(path)

    output_list = []
    for row in gloss_data:
        CN_col = str(row[0])
        TH_col = str(row[1])

        token_list = list(jieba.cut(CN_col, cut_all=False))
        token_list = [ token for token in token_list if len(re.findall(r"[\u4e00-\u9fa5]+", token)) > 0]
        output_list.append(["|".join(token_list)])

    saveData("tokenize_cleaned.xlsx", output_list)

#get_source_target('gloss_test.xlsx')
#gloss_search('./all_xlsx/')

#gloss_clean("./all_xlsx_search_translatePair.xlsx")
gloss_tokenize("cleaned.xlsx")
