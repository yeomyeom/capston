# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import urllib.parse


def setURL(searchWord):
    searchWord = urllib.parse.quote(searchWord)
    URL = (
    "https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&"
    "post_blogurl=&post_blogurl_without=&query={}&sm=tab_pge&srchby=all&st=sim&where=post&start=1".format(searchWord)
    )
    return URL


def getSiteHtml(url):
    # bs4 객체를 반환
    try:
        opened = urlopen(url)
    except (HTTPError, URLError):
        print("Unable to open url.")
        return None
    try:
        html = bs(opened.read(), 'html.parser')
    except AttributeError:
        print("Unable to open url.")
        return None
    return html
    