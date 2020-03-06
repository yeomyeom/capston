from math import log10
import pickle
from knusl import psDetermine
from sklearn.feature_extraction.text import TfidfVectorizer


if __name__ == '__main__':
    fread = open('nonAdvData.txt', 'r', encoding="utf-8")
    line = fread.readlines()
    tfidf_vec = TfidfVectorizer()
    temp = tfidf_vec.fit_transform(line)
    feature_names = tfidf_vec.get_feature_names()
    temp_arr = TfidfVectorizer().fit(line)
   # print(temp_arr.transform(line).toarray())

    #print(temp)
    #print(temp[0])
    #print(type(temp[0]))
    temp_doc = temp.todok()
    temp_dic = dict(temp_doc)
    #print(temp_dic)
    #print(type(temp_dic))
    temp_voca = dict(tfidf_vec.vocabulary_)
    print(temp_voca)
    print(type(temp_voca))

    kor_tfidf_list = []
    for koreanWord, label in temp_voca.items():
        for (i, label_dic) in temp_dic:
            if(label_dic == label):
                print(koreanWord)
                tupletemp = (i,label_dic)
                print(temp_dic.get(tupletemp))
                print('\n')
                kor_tfidf_list.append([koreanWord,temp_dic.get(tupletemp)])
    print(kor_tfidf_list)


    '''for (i,j) in temp_dic:
        print(i,j)
        templist = (i,j)
        print( temp_voca.get() )

    '''
    #print(temp_doc)
    #print(type(temp_doc))
   # print(temp_arr[0][1])
    #print(temp[0])
    #print(type(temp[0]))
    #temtem = temp[0]
    #feature_idx = 0
    '''for i in feature_names: # 여기서 numerate해서 점수
        print(feature_idx,' ',i)
        feature_idx = feature_idx + 1
    '''
    #Mc =temp.tocoo()
    #{k:v for k,v in zip(Mc.col, Mc.data)}
    #print(Mc)
    #print(type(Mc))
    #tfidf_list =[]
    #array = temp.tolist()
      # print(type(temp))

    #print(array)

   # print(temp_arr)
   # print(temp_arr[1])




    #print(feature_names[1])#라벨 값 알아냄
    #print(tfidf_vec.inverse_transform(temp))

    #list1 = ['ㄱ ㄴ ㄷ','ㄴ ㄷ ㅎ','ㄱ ㄴ ㄱ','ㄹ ㄹ ㄹ']
    #tfidf_vectorizer = TfidfVectorizer()
    #tfidf_vectorizer.fit(line)
    #print('list1입니다',tfidf_vectorizer.vocabulary_)


'''
# =======================================
# -- TF-IDF 연산
# =======================================

#tf의 리스트 d 속 t라는 단어가 몇개인지 정수로 리턴한다
def f(t, d):
    return d.count(t)

#tf연산
def tf(t, d):
    # d 문서 하나 -> 여기선 리스트 하나 ->토큰이라 하자
    #w는 d의 각각의 요소.
    #f(t,d)는 d라는 리스트 속 총 단어수
    # max([f(w,d) for w in d])해석 -> 문서 d 속 가장 많이 나온 해당 단어의 갯수 ex) "저는 염승윤입니다"라고 염승윤은 말했다. ->염승윤 이란 단어가 2개로 가장 많이 나옴 -> 리턴값은 2다.
    #return은 tf수치인 정수값이다.
    return 0.5 + 0.5*f(t,d)/max([f(w,d) for w in d])

#idf 연산
def idf(t, D):
    # D 는 문서'들, d의 리스트
    #numerator는 D의 길이(문장의 수)
    #denominator는 특정단어 t가 d의 있는 경우의 길이를 나타낸다
    #return은 idf수치인 정수값이다.
    numerator = len(D)
    denominator = 1 + len([ True for d in D if t in d])
    return log10(numerator/denominator)

#둘이 곱하는 게 tf-idf 점수
#t는 특정단어 스트링
#d는 특정 리스트(1문장)
#D는 문장들의 리스트
#return은 tf-idf수치인 정수값이다.
def tfidf(t, d, D):
    return tf(t,d)*idf(t, D)

#띄어쓰기로 하나씩 잘라 토큰화함
#return은 ['a', 'b', 'c', 'd'] 같은 리스트형이다.
def tokenizer(d):
    # return [ t for t in d.split() if len(t) > 1 ]
    return d.split()


#tfidf수치 연산
#리턴은 result['스트링',tfidf소수값]인 리스트다.
#
#col = 0 or 1
#for i in arr:
#    print(i[col])
#형태로 '스트링' 또는 tfidf소수값에 접근할 수 있다.
def tfidfScorer(D):
    print()
    tokenized_D = D
    result = []
    for d in tokenized_D:
        result.append([(t, tfidf(t, d, tokenized_D)) for t in d])
    return result



if __name__ == '__main__':

    resultList = []
    print('읽기전')
    #
    with open("nonAdvDataKonlpy.pickle","rb") as fr:
        konlpyData = pickle.load(fr)
    print('읽은후')
    print('tfidf값 먹이기 직전')
    for i, doc in enumerate(tfidfScorer(konlpyData)):
        print('====== document[%d] ======' % i)
        print(doc)
        resultList += doc
    print('tfidf값 다 계산됨')

    #중복값이면 tf-idf값은 동일하므로 중복값 있으면 낭비. 제거한다.
    resultList = list(set(resultList))
    #값 큰순으로 소팅하려는데 잘 먹히지 않는 거 같다...
    sorted(resultList, key=lambda doc: doc[1], reverse=True)
    print(resultList)

    #감정값 입력
    idx = 0
    psResultList = []
    for d in resultList:
        print (idx)
        psResultList += d
        psResultList.append(0)
        print (psResultList[idx])
        idx = idx +1
    print (psResultList)


    save_dir = 'nonAdvDataTfidf.pickle'  # 저장 경로
    with open(save_dir, 'wb') as fwrite:
        pickle.dump(psResultList, fwrite)
    fwrite.close()
    #잘 저장되었나 체크
    with open(save_dir, 'rb') as f:
        data = pickle.load(f)  # 한 줄씩 읽어옴

    idx2 =0
    for i in range(10):  # 5줄만 테스트로 읽어옴
        print(idx2)
        print(data[i])
        idx2 = idx2 + 1
    print(data)

'''