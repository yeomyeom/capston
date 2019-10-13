#_*_coding: utf-8 _*_
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import pickle
import os

read_file = './input.txt'
write_file = './output.txt'

def web_parse(url):     # Function of Open HTML.
    try:
         print('web parsing start')
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
    print('firstparse')
    inner_html = []     #inner_html url list
    firsthtml = web_parse(url)   
    links = re.findall('<iframe (.*?)>', firsthtml) # Getting innerhtml link
    for linkElement in links:
        inner_html += re.findall('src="(.*?)"', linkElement)
    print(inner_html)   #inner_html is list of string
    link = inner_html[0]   #no need to parse hidden html(contain blog music)
    return link

def secoundparse(url):  # Second Parsing of REAL URL
    print('secoundparse')
    pics, stickers, texts, text = [],[],[],[]  # arrays of pic, sticker, text.
    secondhtml = web_parse(url)
    #pics += re.findall('<img.*?src="(.*?)".*?data-width="(.*?)" data-height="(.*?)".*?>', secondhtml) #parse pics number
    pics += re.findall('<img.*?src="(.*?)".*?>', secondhtml) #parse pics number
    #stickers += re.findall('<img.*? src="(.*?)".*?class="se-sticker-image" />',secondhtml)  #parse sticker number
    stickers += re.findall('<img.*? src="(.*?)".*?class="se-sticker-image" />',secondhtml)  #parse sticker number
    text += re.findall('<span.*?>(.*?)</span>',secondhtml) #parse text
    
    for parse in text:
        texts += re.findall("[가-힝 ]",parse)

    filelist = os.listdir('./')
    i = 0
    for item in filelist:
        if item.find(str(i)) is -1:#if contenti.txt is not exist
            with open('content'+str(i)+'.txt', 'wb') as file1:
                pickle.dump(text, file1)
            with open('picture'+str(i)+'.txt', 'wb') as file2:
                pickle.dump(pics, file2)
            with open('sticker'+str(i)+'.txt', 'wb') as file3:
                pickle.dump(stickers, file3)
        else:
            print('content'+str(i)+'.txt exist')
            i = i + 1


def exceptionparse(url):
    print('exceptionparse')
    inner_html = []     #inner_html url list
    firsthtml = web_parse(url)   
    links = re.findall('<iframe (.*?)>', firsthtml) # Getting innerhtml link
    for linkElement in links:
        inner_html += re.findall('src=\'(.*?)\'', linkElement)
    print(inner_html)  #inner_html is list of string 
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
    f = open(read_file,'r')
    url_num = f.readline()
    for i in range(0,int(url_num)):
        url = f.readline()
        Parse(url)
    f.close()

"""     BeautifulSoup is too slow to use parsing program """
