# -*- coding: utf-8 -*-
from CrawlFunction import setURL, getSiteHtml



################################################################

def CrawlURL(searchWord, MAX_NUMBER_TO_SEARCH):
    maxnum = int(MAX_NUMBER_TO_SEARCH/10)
    url = setURL(searchWord)
    f = open("TestModule/CrawlResult.txt", "w", encoding='utf8')

    for i in range(1,maxnum+1):
        html = getSiteHtml(url)
        results = html.findAll('li',{'class':'sh_blog_top'})

        for result in results:
            title = result.find('a',{'class':'sh_blog_title _sp_each_url _sp_each_title'})
            title = title['href']+'\n'
            f.write(title)

        try:
            url = "https://search.naver.com/search.naver"+html.find('a',{'class':'next'})['href']
        except TypeError:
            print("Crawling stopped at page {}.".format(maxnum))
            break
    f.close()


