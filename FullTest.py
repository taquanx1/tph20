import classLib.fileClass as file
import classLib.gloss as gs
from datetime import datetime

start = datetime.now()

test_ori = file.xl01("陈先生-5W.xlsx", "test_file1", 'C')
test_corpus = test_ori.to_corpus()
new_gloss = gs.gloss('gloss2_test - 副本.xlsx', gloss_name='Test_glossy')
test_corpus.add_gloss(new_gloss)
test_corpus.export_to_xlsx()

end = datetime.now()
print("------------------------------------\nFullTest time: %sms"%(end-start).seconds)

'''
gloss:
Reducing: 91.460204% (44114/48233)
Using: 0.612979s

Non gloss:
Reducing: 77.017809% (37148/48233)
Using: 0.725713s


Preprocessing finish!
Remaining: 86.173367% (41564/48233)
Using: 0.110891s

Preprocessing finish!
Remaining: 68.152510% (32872/48233)
Using: 0.647927s

Preprocessing finish!
Remaining: 50.633384% (24422/48233)
Using: 0.107987s
'''


'''
0:
Remaining: 41.886260% (20203/48233)
Using: 0.143226s
84


'''