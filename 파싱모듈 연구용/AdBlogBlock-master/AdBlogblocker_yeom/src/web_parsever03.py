#web parsing with beautifulsoup
#from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import js2py

def web_parse(url):
    try:
         print('start')
         html = urlopen(url).read().decode('utf-8')
    except HTTPError as e:
        print('fail : ',e.reason)
        html = None
    return html
def get_targeturl(url):
    host_url = re.findall('https://(.*?)/',url)
    target_url = 'https://'+host_url[0]
    return target_url
def main():
    inner_html = []#inner_html url list
    pics = [] #inner_html's pictures url
    num_pic = 0 #pictures number
    sticker = [] #inner_html's sticker url
    num_sticker = 0#stickers number
    text = []#inner_html's texts
    num_text = 0
    #url = 'https://blog.naver.com/dragon1086/221037326999'
    url = 'https://blog.naver.com/cwy5114/221492558752'
    #url = 'https://blog.naver.com/my_prayer_s2/221493594784'
    target_url = get_targeturl(url)
    html = web_parse(url)
    link = re.findall('<iframe (.*?)>', html)
    for links in link:
        inner_html += re.findall('src="(.*?)"', links)
    print(inner_html) #inner_html is list of string
    links = inner_html[0]#no need to parse hidden html(contain blog music)
    links = target_url+links
    html = web_parse(links)
    pics += re.findall('<img src="(.*?)".*?data-width="(.*?)" data-height="(.*?)".*?class="se-image-resource" />', html)#parse pics number
    sticker += re.findall('<img.*? src="(.*?)".*?class="se-sticker-image" />',html)#parse sticker number
    text += re.findall('<span.*?>(.*?)</span>',html)#parse text
    #print(pics)
    #print(sticker)
    num_pic += len(pics)
    num_sticker += len(sticker)
    num_text += len(text)
    print(num_pic)
    print(num_sticker)
    print(num_text)
    for texts in text:
       print(texts)
    #BeautifulSoup is too slow to use parsing program
    #for links in link:
    #    print(links)
    #    html = web_parse(links)
    #soup = BeautifulSoup(html,'html5lib')
    #fixed_html = soup.prettify()
    #print(fixed_html)
