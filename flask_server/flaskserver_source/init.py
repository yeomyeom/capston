from flask import Flask
from flask import request
from flask_cors import CORS
#pip install flask_cors
from urllib.request import urlopen
from urllib.error import HTTPError
import json
import re
import pickle
import os

app = Flask(__name__)
CORS(app)

def web_parse(url):     # Function of Open HTML.
      try:
            html = urlopen(url).read().decode('utf-8')
      except HTTPError as e:
            html = None
      return html

def parse(url):  # Second Parsing of REAL URL
      pics, stickers, texts, text = [],[],[],[]  # arrays of pic, sticker, text.
      html = web_parse(url)
      try:
            #pics += re.findall('<img.*?src="(.*?)".*?data-width="(.*?)" data-height="(.*?)".*?>', secondhtml) #parse pics number
            pics += re.findall('<img.*?src="(.*?)".*?>', html) #parse pics number
            #stickers += re.findall('<img.*? src="(.*?)".*?class="se-sticker-image" />',secondhtml)  #parse sticker number
            stickers += re.findall('<img.*? src="(.*?)".*?class="se-sticker-image" />',html)  #parse sticker number
            text += re.findall('<span.*?>(.*?)</span>',html) #parse text
          
            for parse in text:
                  texts += re.findall("[가-힝0-9:.# ]",parse)
            return texts
      except:
            return None

#===============================================================================
@app.route("/<url>")
def template_test(url):
      #url 받아서 파싱-완료
      url = "https://blog.naver.com/PostView.nhn?" + url
      texts = []
      texts = parse(url)
      #result = " ".join(texts)

      #파싱된 파일들을 가지고 점수 출력
      emotion = -0.75
      title = 0.5
      link = ['https://weble.com', 'https://ad.com']
      sticker = ['https://naver.com/stickerasd', 'https://naver.com/sticker23123']
      same = []
      tag = 0.9
      result ={
            'Emotion':emotion,
            'Title':title,
            'Link':link,
            'Sticker':sticker,
            'Same':same,
            'Tag':tag
            }
      
      #해당 점수를 가지고 결과를 json 형태로 전송
      jsonstr = json.dumps(result)
      return jsonstr;

@app.route("/error")
def error():
      result = "네이버 블로그가 아닙니다."
      return result

if __name__=="__main__":
      app.run(port=5001)
