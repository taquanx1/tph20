import pickle

corpus_filename = '陈先生-5W.tqcp'
f = open(corpus_filename, 'rb')
data = pickle.load(f)
f.close()

data.export_to_xlsx("curpus_test_%s.xlsx")