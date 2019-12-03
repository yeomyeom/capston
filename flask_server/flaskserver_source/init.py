from flask import Flask
from flask import request
from flask_cors import CORS
#pip install flask_cors
from urllib.request import urlopen
from urllib.error import HTTPError

from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2, SelectKBest
from joblib import load
from konlpy.tag import Okt

import json
import re
import pickle
import os
import numpy
import time, datetime

application = Flask(__name__)
CORS(application)

def loading():
    print("load start\n")
    global model
    global count_vec
    global tf_trans
    global selectChi
    global advList
    global nonAdvList
    global posi
    global nega
    global posiList
    global negaList
    global advImageUrl
    global advImageList
    global babyList
    global itList
    global restList
    
    model = load('mlmodel.joblib')
    count_vec = load('countvec.joblib')
    tf_trans = load('tf_trans.joblib')
    selectChi = load('select.joblib')
    
    with open('sticker_adv.pickle','rb') as file:
        advList = pickle.load(file)
    with open('sticker_nonAdv.pickle','rb') as file2:
        nonAdvList = pickle.load(file2)
        
    posi = open("posiList.txt",'r',encoding='utf-8')
    nega = open("negaList.txt",'r',encoding='utf-8')
    posiList = posi.readlines()
    negaList = nega.readlines()
    
    advImageUrl = open("picture_adv_UTF-8.txt", 'r', encoding='UTF-8')
    advImageList = advImageUrl.readlines()

    with open('categ_baby.txt','r',encoding='UTF-8') as baby:
        babyList = baby.readlines()
    with open('categ_it.txt', 'r', encoding='UTF-8') as it:
        itList = it.readlines()
    with open('categ_restaurant.txt', 'r', encoding='UTF-8') as rest:
        restList = rest.readlines()


    print("load finish\n")
    
def title_content_check(texts):
    # 1
    content = texts
    full_content = texts
    # 2
    try:
        contentArr = content.split('목록열기')
        content = contentArr[1]
        content = content[0:25]
    except:
        try:
            contentArr = content.split('퀵에디터가 오픈했어요')
            content = contentArr[1]
            content = content[0:40]
        except:
            content = 'unknown'

        okt = Okt()
        tag_token_list = okt.nouns(content)


    # 3
    #konlpy 처리
    okt = Okt()
    title_token_list = okt.nouns(content)
    #print("Title : " + title_token_list)

    # 4
    # title_token_list에서 제목 단어 수 세서 출력
    usefulWordCount = 0

    title_used = 0
    for i in title_token_list:
        temp = full_content.count(i)
        title_used += temp
    #print('제목 단어 수',len(title_token_list))

    print("Title : ")
    print(title_token_list)
    # 6 출력
    # 제목단어 사용률/전체 단어

    try:
        ratio = round(temp/len(full_content.split()),3)
    except:
        ratio = 0
    #print(ratio)
    return ratio

# tag_content_check()
# 1.content.txt 내용을 content 변수에 단일 스트링형식으로 담는다.
# 2.제목이 있을만한 쪽을 추출해낸다
# 3.주제 연관도에 쓸 명사 토큰만 추출
def tag_content_check(texts, taglist):
    # 1

    full_content = texts
    contentForTag = texts
    # 2
    #halfContentLen: content 스트링의 길이/2 저장
    #ContentLen: content 스트링의 길이 저장
    ''' 
    halfContentLen = round(len(contentForTag)/2)
    contentLen = len(contentForTag)

    temp = contentForTag[halfContentLen:contentLen-1]
    #print(temp)
    contentForTagArr = temp.split('#')
    #print(contentForTagArr)
    idx = 0
    tags = []
    for j in enumerate(contentForTagArr):
        if(j[0]==0):
            print()# 앞에 불필요한걸 자른다
        if(j[0] == len(contentForTagArr)-1):
            #print(j[1][0:7])
            tags.append(j[1][0:7])
        else:
            #print(j[0])
            tags.append(j[1])
    print(tags)
    '''
    tags = taglist
    okt = Okt()
    tags_string =''
    for z in tags:
        tags_string += z
    tags_konl = okt.nouns(tags_string)
    #print(tags_konl)

    full_content_temp = full_content
    useful_word_count = 0
    for i in tags_konl:
        temp = full_content.count(i)
        #print(temp)
        useful_word_count += temp
    #print('태그 단어 수',len(tags_konl))
    print("tag:")
    print(tags_konl)
    return round( useful_word_count/len(full_content_temp.split()),3)

# sticker.txt에서 광고성 스티커와 비광고성 스티커의 비율을 구해 출력한다(double형)
# 1. 필요한 파일을 열고 저장한다 (광고성/비광고성은 list로. 사용자 sticker는 단일string으로)
# 2. 광고성/비광고성 스티커 개수를 저장할 advNum과 nonAdvNum 변수를 생성한다
# 3. for문으로 사용자 sticker 속 광고성/비광고성 스티커 개수를 세서 변수에 저장한다
# 4. 광고성/비광고성 비율을 출력, 비광고성이 0일 경우 광고성 개수 * (-1)을 출력한다. 출력값이 0이면 광고성 스티커가 없다는 뜻이다.
def advStickerRatio(stickers):
    #with open('sticker_adv.pickle','rb') as file:
        #advList = pickle.load(file)
    #with open('sticker_nonAdv.pickle','rb') as file2:
        #nonAdvList = pickle.load(file2)
    userStickerString = stickers
    result = []
    #print(userStickerString)

    advNum = float(0)
    nonAdvNum = float(0)

    for i in advList:
        if( i in userStickerString):
            #advNum += 1
            result.append(i)
    for j in nonAdvList:
        if( j in userStickerString):
            #nonAdvNum += 1
            #result.append(j)
    print("sticker urls")
    print(result)
    #if(nonAdvNum == 0): return advNum * -1
    #else: return advNum/nonAdvNum
    return result

def posi_nega_check(texts):
    #posi = open("posiList.txt",'r',encoding='utf-8')
    #nega = open("negaList.txt",'r',encoding='utf-8')
    
    content = texts

    posiNum = float(0)
    negaNum = float(0)
    for posIdx in posiList:

        posiNum +=content.count(posIdx[:-1])
    for negIdx in negaList:

        negaNum +=content.count(negIdx[:-1])
    print("pos num" + str(posiNum))
    print("neg num" + str(negaNum))
    if (negaNum == 0): return posiNum * -1
    else: return posiNum/negaNum

def advImageChecking(pics):
    userImageList = pics
    newUIU = []
    newUIU2 = []
    #advImageUrl = open("picture_adv_UTF-8.txt", 'r', encoding='UTF-8')
    #advImageList = advImageUrl.readlines()
    newAIU = []
    newAIU2 = []
    newAIU3 = []
    result = []
    #print(userImageList)
    #print(advImageList)
    for i in userImageList:
        newUIU += i.split()
    for j in newUIU:
        newUIU2 += j.split('\n')
    #print(newUIU2)

    for k in newUIU2:
        for l in advImageList:
            if(k in l): result.append(k)
    print("img url: ")
    print(result)
    #2
    #okt = Okt()
    #temp = []
    #for t in userImageList:
    #    temp.append(okt.nouns(i))
    #    #print(temp[0])
    #    if(len(temp) != 0): result.append(t)

    return result

def categorizing(texts):
    content = texts
    #with open('categ_baby.txt','r',encoding='UTF-8') as baby:
        #babyList = baby.readlines()
    #with open('categ_it.txt', 'r', encoding='UTF-8') as it:
        #itList = it.readlines()
    #with open('categ_restaurant.txt', 'r', encoding='UTF-8') as rest:
        #restList = rest.readlines()

    babyNum = 0
    itNum = 0
    restNum = 0

    for i in babyList:
        babyNum += content.count(i[:-1])
    for j in itList:
        itNum += content.count(j[:-1])
    for t in restList:
        restNum += content.count(t[:-1])

    tempList = [babyNum,itNum,restNum]
    if( max(tempList) == babyNum): return 1
    elif( max(tempList) == itNum): return 3
    else: return 2
    #출력값 1: 육아
    #출력값 3: it
    #출력값 2: 맛집

def sendVal(texts, pics, stickers, taglist):
    # 0. 카테고리 정하기
    categNum = categorizing(texts)

    # 1.
    # 육아: 빨: 1.5, 음수값     초:0.96
    # 맛집: 빨: 2.6  음수값     초: 2.1
    # it    빨: 2.4             초: 1.26
    # 뷰티  빨: 2.33            초: 1.49
    #그 사이는 노랑이다
    advPosiNega = posi_nega_check(texts)
    #print("긍부정어비율: ", advPosiNega)

    #psColor = 0
    '''
    if(categNum == 1):
        if(advPosiNega > 1.5 or advPosiNega < 0.0): psColor = 1 # 빨강
        elif(advPosiNega < 0.96 and advPosiNega >= 0): psColor = 3 # 초록
        else: psColor = 2 #노랑
    elif(categNum == 2):
        if (advPosiNega > 2.6 or advPosiNega < 0.0):
            psColor = 1  # 빨강
        elif (advPosiNega < 2.1 and advPosiNega >= 0):
            psColor = 3  # 초록
        else:
            psColor = 2  # 노랑
    elif(categNum == 3):
        if (advPosiNega > 1.5 or advPosiNega < 0.0):
            psColor = 1  # 빨강
        elif (advPosiNega < 0.96 and advPosiNega >= 0):
            psColor = 3  # 초록
        else:
            psColor = 2  # 노랑
        # it    빨: 2.4             초: 1.26
        # 뷰티  빨: 2.33            초: 1.49
    else:
        if (advPosiNega > 2.33 or advPosiNega < 0.0):
            psColor = 1  # 빨강
        elif (advPosiNega < 1.49 and advPosiNega >= 0):
            psColor = 3  # 초록
        else:
            psColor = 2  # 노랑
    '''

    # 2.


    # 3.
    # :빨: 1    ,konlpy한글(빨강으로 하자): 2       초: 0
    advImgList = advImageChecking(pics)
    #print("광고성그림유무: ", advImgNum)
    #advImgColor = 0
    '''
    if (advImgNum == 1):advImgColor = 1 #빨강
    elif(advImgNum == 2): advImgColor =4 #konlpy 광고성 매우 의심 빨강
    else: advImgColor = 3#초록색
    '''

    # 4.
    # 빨: 값 < -3 or 2.5<값                          초:    0 =<값< 0.5
    advStickerList = advStickerRatio(stickers)
    #print("광고성/비광고성 스티커 비율: ", advStickerRatio)
    #advStickerColor = 0
    '''
    if (advStickerRatio < -3 or 2.5<advStickerRatio): advStickerColor = 1 #빨강
    elif(advStickerRatio<0.5 and advStickerRatio>=0): advStickerColor = 3 #초록
    else: advStickerColor = 2 #노랑
    '''

    # 5. float형 소수점 3자리
    # 빨:0.06 이상  초:0.004이하
    tagValue = tag_content_check(texts, taglist)
    #print("태그-본문연관성: ", tagValue)
    #tagColor = 0
    '''
    if(tagValue > 0.06): tagColor = 1 #빨강
    elif(tagValue<0.004 and tagValue>=0): tagColor = 3 #초록
    else: tagColor = 2 #노랑
    '''

    # 6. float형 소수점 3자리
    # 빨:0.021 이상  초: 0.002이하
    titleValue = title_content_check(texts)
    #print("타이틀-본문연관성", titleValue)
    '''
    titleColor = 0
    if(titleValue >= 0.021): titleColor = 1 #빨강
    elif(titleValue < 0.002 and titleValue >=0): titleColor = 3 #초록
    else: titleColor = 2 #노랑
    '''
    return categNum, advPosiNega, advImgList , advStickerList, tagValue, titleValue

def mlmodel(texts):
    #model = load('mlmodel.joblib')
    #count_vec = load('countvec.joblib')
    #tf_trans = load('tf_trans.joblib')
    #selectChi = load('select.joblib')
    count = count_vec.transform(texts)
    cut = selectChi.transform(count)
    tfval = tf_trans.transform(cut)
    arr = model.predict_proba(tfval)
    nn = arr.tolist()[0]
    return nn

def web_parse(url):     # Function of Open HTML.
    try:
        html = urlopen(url).read().decode('utf-8')
    except HTTPError as e:
        html = None
    return html

#===============================================================================
@application.route("/<url>")
def template_test(url):
    #url 받아서 파싱
    now = datetime.datetime.now()
    start = time.time()
    url = "https://blog.naver.com/PostView.nhn?" + url
    pics, stickers, texts, text, taglist = [],[],[],[],[]  # arrays of pic, sticker, text 
    html = web_parse(url)
    pics += re.findall('<img.*?src="(.*?)".*?>', html) #parse pics number
    stickers += re.findall('<img.*? src="(.*?)".*?class="se-sticker-image" />',html)  #parse sticker number
    text += re.findall('<span.*?>(.*?)</span>',html) #parse text
    taglist += re.findall('<span class="__se-hash-tag">#(.*?)</span>', html)
    print("tag list")
    print(taglist)
    for parse in text:
        texts += re.findall("[가-힝# ]",parse)
    text = "".join(texts)
    texts = []
    texts.append(text)
    #result = " ".join(texts)
    #파싱된 파일들을 가지고 점수 출력
    models = mlmodel(texts)
    categnum, emotion, link, sticker, tag, title = sendVal(text,pics,stickers,taglist)
    #text는 문자열, pics 리스트, stickers 리스트
    #categNum, advPosiNega, 0, advImgList , advStickerList, tagValue, titleValue
    result ={
          'Categnum':categnum,
          'Emotion':emotion, # -1(negative emotion) ~ +1(positive emotion)
          'Title':title,     # 0 ~ 1 (keyword match rate)
          'Link':link,       # [img URL1, img URL2, ...]
          'Sticker':sticker, # [sticker URL1, sticker URL2, ...]
          'Tag':tag,         # 0 ~ 1 (keyword match rate)
          'Model':models     # adv or nadv
          }
    
    #해당 점수를 가지고 결과를 json 형태로 전송
    end = time.time()
    elasped = end - start
    f = open("timelog.log", 'a')
    f.write(str(now) + ' Lead time :' + str(elasped) + ' sec\n')
    f.close()
    jsonstr = json.dumps(result)
    return jsonstr;

@application.route("/error")
def error():
    result = "네이버 블로그가 아닙니다."
    return result

if __name__=="__main__":
    loading()
    application.run(host="0.0.0.0")
