import pickle

#1. tfidf_calculating에서 처리된 광고성.pickle과 비광고성.pickle을 가져온다.
#2. 명사, 동사, 형용사, 부사 등 제한된 종류의 단어만 걸러낸다
#3. O(n^n)이겠지만, 둘이 겹칠 경우 a^b 리스트(intersection)에 저장
#4. 나머지 광고성은 advlist에, 비광고성은 nonadvlist에 저장.
#5. 세가지 값을 각각 .pickle로 저장.


#2
def listAdjust(advlist):
    #2-pre tfidf값으로 미리 의미있는 형태소만 골라낸다
    idx_pre = 0
    temp = advlist
    temp.append(advlist)
    meaningful_advlist_data =[]
    for j in enumerate(temp):
        if ((idx_pre%3 == 1) and j[1] > 0.11): # j[1] >0.11 은 tfidf값이 0.11 이상인 값만 골라냄
            print(temp[idx_pre-1])
            meaningful_advlist_data.append(temp[idx_pre-1])
        idx_pre = idx_pre + 1
    #2 리스트 형태 [(3n-2)->('형태소','Noun/Verb/Adjective'), (3n-1)->tfidf값, (3n)감정값]
    print("의미있는 형태소만 뽑아냄",meaningful_advlist_data)

    idx = 0
    adjusted_advlist_data = [0]

    for i in meaningful_advlist_data:
        if((i[1] == 'Noun' or i[1] == 'Verb' or i[1] == 'Adjective')): #3의 배수마다 형태소리스트가 있으므로 체크
             # 해당 형태소가 Noun/Verb/Adjective면 adjusted_advlist_data에 추가
            adjusted_advlist_data.append(i)
        idx = idx+1
    del adjusted_advlist_data[0] #초기화를 위해 썼던 data[0]값 삭제
    print(adjusted_advlist_data)

    return adjusted_advlist_data

#3
def extract_intersection(advlist, nonadvlist):
    intersection = set(advlist)&set(nonadvlist)
    #for i in advlist:
    #    for j in nonadvlist:
    #        if(i[0] == j[0]):
    #            intersection.append(j)
    #del intersection[0]
    #return intersection
    print(advlist)
    print(nonadvlist)
    print( "extract_intersection완료 ->",intersection)
    t1 = list(intersection)
    return t1

#4 list는 advlist나 nonadvlist
def extract_difference(list, intersection):
    difference = set(list)-set(intersection)
    t1 = []
    for i in difference:
        t1.append(i)
    return t1
    #for i in list:
    #    if((i[0] not in intersection)):
    #        difference.append(i)
    #del difference[0]
    #return difference


if __name__ == '__main__':
    # 1
    with open("advDataTfidf.pickle", "rb") as advlist:
        advlist_data = pickle.load(advlist);
    with open("nonAdvDataTfidf.pickle", "rb") as nonadvlist:
        nonadvlist_data = pickle.load(nonadvlist);
    advtemp = advlist_data
    nonadvtemp = nonadvlist_data
    print("정렬전 advlist_data",advtemp)
    print("정렬전 nonadvlist_data",nonadvtemp)
    adjusted_advlist = listAdjust(advtemp)                                #2
    adjusted_nonadvlist = listAdjust(nonadvtemp)                          #2
    print("정렬후 adjusted_advlist", adjusted_advlist)
    print("정렬후 nonadjusted_advlist", adjusted_nonadvlist)
    intersection = extract_intersection(adjusted_advlist, adjusted_nonadvlist)  #3
    adv_difference = extract_difference(adjusted_advlist, intersection)      #4
    nonadv_difference = extract_difference(adjusted_nonadvlist, intersection) #4

    print("최종",intersection)
    print(adv_difference)
    print(nonadv_difference)


    dir_list = [0]
    save_dir1 = 'intersection.pickle'  # 저장 경로
    save_dir2 = 'adv_difference.pickle'
    save_dir3 = 'nonadv_difference.pickle'

    with open(save_dir1, 'wb') as fwrite1:                                  #5
        pickle.dump(intersection, fwrite1)
    fwrite1.close()
    with open(save_dir2, 'wb') as fwrite2:
        pickle.dump(adv_difference, fwrite2)
    fwrite2.close()
    with open(save_dir3, 'wb') as fwrite3:
        pickle.dump(nonadv_difference, fwrite3)
    fwrite3.close()

