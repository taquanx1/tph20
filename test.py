from utils.expy import getColumn, getData
from datetime import datetime

start = datetime.now()

gloss_path = './gloss/RO_gloss.xlsx'
CHN = getColumn(gloss_path, 'A', 1, 1)
THA = getColumn(gloss_path, 'B', 1, 1)
gloss_list = [ [c, t] for c, t in zip(CHN, THA)]
#gloss_list = getData(gloss_path)

gloss_list = sorted(gloss_list, key= lambda x:len(x[0]), reverse = True)
gloss_list = zip(*gloss_list)
gloss_list = list(map(list, gloss_list))
CHN = gloss_list[0]
THA = gloss_list[1]

end = datetime.now()
for c, t in zip(CHN, THA):
    print(c, t, len(c))

#for item in gloss_list:
#    print(item ,len(item[0]))

print(end - start)

'''
41
20
'''