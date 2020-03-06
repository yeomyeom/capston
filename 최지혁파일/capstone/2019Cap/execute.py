import konlpyForExecuting
import collections
import tfidf_calculating
import word_venn_diagram
import pickle


#0 블로그의 크롤링 데이터를 받았다고 가정한다
#0 필요한 데이터 미리 받아온다

#1 블로그의 크롤링 데이터를 konlpy 전처리를 한다
#1 입력값: dataForExecution.txt
#1 출력값: dfeKonlpy.pickle로 저장된다

#2 tfidf값으로 광고성 점수 판단
#2 입력값:

#0 - 1.교집합 리스트, 2.adv집합 리스트와 3.nonadv집합 리스트를 가져온다
save_dir1 = 'intersection.pickle'  # 저장 경로
save_dir2 = 'adv_difference.pickle'
save_dir3 = 'nonadv_difference.pickle'
with open(save_dir1, "rb") as f1:
    intersection = pickle.load(f1)
print("교집합",intersection)
with open(save_dir2, "rb") as f2:
    adv_difference = pickle.load(f2)
print("광고성 차집합",adv_difference)
with open(save_dir3, "rb") as f3:
    nonadv_difference = pickle.load(f3)
print("비광고성 차집합",nonadv_difference)
with open("advDataTfidf.pickle", "rb") as f4:
    advDataTfidf = pickle.load(f4)
print("광고성Tfidf",advDataTfidf)
with open("nonAdvDataTfidf.pickle", "rb") as f5:
    nonAdvDataTfidf = pickle.load(f5)
print("비광고성Tfidf",nonAdvDataTfidf)
#각각 intersection, adv_difference, nonadv_difference 리스트에 저장된다

#1
data_dir = 'dataForExecution.txt'
konlpyForExecuting.konlpy_pre(data_dir)
# dfeKonlpy.pickle 에 저장된다

#2
#dfe는 tfidf, 벤다이어그램 판단용
with open("dfeKonlpy.pickle", "rb") as advlist:
    advlist_data = pickle.load(advlist);
print("konlpy전처리후: ",advlist_data)

advNum = 0
temp = []
for i in advlist_data:
    temp += i
for i in temp:
    if i in adv_difference:
        advNum = advNum+1
print("temp보기: ",temp)
print ("광고성 단어는 : ",advNum, " 입니다\n")

nonAdvNum = 0
for j in temp:
    if j in nonadv_difference:
        nonAdvNum = nonAdvNum + 1
print ("비광고성 단어는 : ",nonAdvNum, " 입니다\n")
#with open("picture0.txt") as advPic:
#    picUrl = pickle.load(advPic)










