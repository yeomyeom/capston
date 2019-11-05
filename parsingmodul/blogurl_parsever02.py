from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError
import re
import pickle
import os


iteration = 999
keyword = "맛집"


maturl = "https://search.naver.com/search.naver?query="
maturl = maturl + quote(keyword)
maturl = maturl + "&sm=tab_pge&srchby=all&st=sim&where=post&start="
links = []
for i in range(1,iteration):
      url = maturl + str(i)
      print(url)
      try:
           print('web parsing start')
           html = urlopen(url).read().decode('utf-8')
      except HTTPError as e:
           print('fail : ',e.reason)
           html = None
      links += re.findall('<a class="sh_blog_title _sp_each_url _sp_each_title" href="(.*?)".*?</a>',html)
      file = open('url.txt','w')
      file.write('\n'.join(links))
      file.write('\n')
      file.close()
      print(i,' finished')
                         
