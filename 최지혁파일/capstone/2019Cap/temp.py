import pickle

with open("advDataKonlpy.pickle", "rb") as fr:
    konlpyData = pickle.load(fr)
print(konlpyData)

list = []
list.append(konlpyData)
print(list)