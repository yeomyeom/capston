#web parsing with beautifulsoup
#_*_coding: utf-8 _*_
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import js2py
from  CrawlFunction import getSiteHtml
read_file = 'TestModule/CrawlResult.txt'
write_file = 'TestModule/parsed.txt'

def garbageCut(texts, isFirst, string):
    # string is always '본문 기타 기능' or '이 글에 공감한 블로거 열고 닫기' 
    try:
        idx = texts.index(string)
    except ValueError:  #모바일에서 작성한 글일 경우 특수한 처리가 필요함.
        string = '모바일에서 작성된 글입니다.'
        idx = texts.index(string)
    finally:
        if isFirst is True:
            texts = texts[idx+1:]
            return texts
        else:
            texts = texts[:(idx-1)]
            return texts



def web_parse(url):     # Function of Open HTML.
    try:
         html = urlopen(url).read().decode('utf-8')
    except HTTPError as e:
        print('fail : ',e.reason)
        html = None
    return html

def get_targeturl(url):      # Function of loading URL.
    host_url_https = re.findall('https://(.*?)/',url)
    host_url_http = re.findall('http://(.*?)/',url)
    if host_url_https:
        target_url = 'https://'+host_url_https[0]
    else:
        target_url = 'http://'+host_url_http[0]
    return target_url

def firstparse(url):    # Fisrt Parsing to find REAL URl (in #document) 
    inner_html = []     #inner_html url list
    firsthtml = web_parse(url)   
    links = re.findall('<iframe (.*?)>', firsthtml) # Getting innerhtml link
    for linkElement in links:
        inner_html += re.findall('src="(.*?)"', linkElement)
    link = inner_html[0]   #no need to parse hidden html(contain blog music)
    return link

def secoundparse(url):  # Second Parsing of REAL URL
    # For Checking if the html contains Naver Map element
    html = getSiteHtml(url)
    result = html.find('iframe',{'title':'포스트에 첨부된 지도'})
    if result is not None:
        return

    pics, stickers, texts, text = [], [] ,[], [] # arrays of pic, sticker, text.
    secondhtml = web_parse(url)  
    #pics += re.findall('<img src="(.*?)".*?data-width="(.*?)" data-height="(.*?)".*?class="se-image-resource" />'
                        #, secondhtml) #parse pics number
    pics += re.findall('<img.*?src="(.*?)".*?data-width="(.*?)" data-height="(.*?)".*?>'
                        , secondhtml) #parse pics number
    stickers += re.findall('<img.*? src="(.*?)".*?class="se-sticker-image" />',secondhtml)  #parse sticker number
    text += re.findall('<span.*?>(.*?)</span>',secondhtml) #parse text

    # find garbage index : '본문 기타 기능'
    text = garbageCut(text, True, '본문 기타 기능')
    text = garbageCut(text, False, '이 글에 공감한 블로거 열고 닫기')

    pattern = re.compile('[ ]?[<].*')
    for line in text:
        if pattern.match(line):
            continue
        if line in ('','\u200b') :
            continue
        else:
            texts.append(line)

    # for parse in text:
    #     texts += re.findall("[가-힝 ]",parse)
    f = open(write_file,'a',-1,'utf-8')

    for sentence in texts:
        f.write(sentence+'\n')

    f.write('\n')
    f.write('pics : ')
    f.write(str(len(pics)))
    f.write('\n')
    f.write('stickers : ')
    f.write(str(len(stickers))+'\n')
    f.close()

def exceptionparse(url):
    inner_html = []     #inner_html url list
    firsthtml = web_parse(url)   
    links = re.findall('<frame (.*?)>', firsthtml) # Getting innerhtml link
    for linkElement in links:
        inner_html += re.findall('src=\'(.*?)\'', linkElement)
    link = inner_html[0]  #no need to parse hidden html(contain blog music)
    return link

# Main function of "Parsing Phase"
def Parse(url):  # url = "https://blog.naver.com/~~~"
    target_url = get_targeturl(url)
    if re.match('https://blog.naver.com*.?',target_url):
        link = target_url+firstparse(url)
        secoundparse(link)
    elif re.match('https://m.blog.naver.com*.?',target_url):
        secoundparse(url)
    else:
        link = exceptionparse(url)
        target_url = get_targeturl(link)
        link = target_url + firstparse(link)
        secoundparse(link)


# Lines for Simple debugging.
if __name__ == "__main__":

    url = 'https://blog.naver.com/epumna/221488195204'
    Parse(url)




    # f = open(read_file,'r')
    # url_num = f.readline()
    # for i in range(0,int(url_num)):
    #     url = f.readline()
    #     Parse(url)
    # f.close()