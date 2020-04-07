import urllib.request as request
import base64
from bs4 import BeautifulSoup
from urllib import parse

import json
import time


def get_english_name():
    url = "https://dict.naver.com/name-to-roman/translation/?query={}&y=0&where=name".format(parse.quote('박현진'))
    req = request.Request(url=url, method='GET')
    with request.urlopen(req) as f:
        html = '\n '.join([ l.decode('utf-8') for l in f.readlines()])
        bs = BeautifulSoup(html,'html.parser')
        for obj in bs.find_all("td", {"class":"cell_engname"}):
            print(obj.text)

get_english_name()

