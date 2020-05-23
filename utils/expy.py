#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
#
#  TQ_Translate 20170619
#  Excel files IO code
#  *for first Sheet only!
#
######################################
from pyexcel_xls import get_data
from pyexcel_xlsxw import save_data
from collections import OrderedDict

def saveData(file_name, data):
	data_out = OrderedDict()
	data_out .update({"Sheet1": data})
	try:
		save_data(file_name, data_out )
	except Exception as e:
		raise e
		print(e)
		print("Error")

def getData(filepath, sheet_num = 0):
	data = get_data(filepath)
	data_sheet = [ sheet for sheet in data ]
	if sheet_num == 0:
		return [ data[sheet] for sheet in data_sheet ][0]
	else:
		return data[data_sheet[sheet_num-1]]

def getSheetlist(filepath):
	data = get_data(filepath)
	return [ sheet for sheet in data ]

def getColumn(filepath, column = 'A', sheet = 1, mode=0):
	data = getData(filepath, sheet)
	data_out = []
	if mode == 0:
		for item in data:
			try:
				data_out.append([item[ord(column)-65]])
			except:
				data_out.append([''])
		return data_out
	if mode == 1:
		for item in data:
			try:
				data_out.append(item[ord(column)-65])
			except:
				data_out.append('')
		return data_out	
		
def count(filepath, column = 'A', sheet = 1):
	column = getColumn(filepath, column, sheet)
	count = 0
	for item in column:
		try:
			count += len(item)
		except Exception as e:
			pass
	return count
