# coding=utf-8
import sys
import urllib
import urllib.request
import re
from urllib.parse import quote


def baidu_search(keyword):
    keyword = quote(keyword)
    url = "http://www.baidu.com/s?wd={}".format(
        keyword)
    print(url)
    res = urllib.request.urlopen(url)
    html = res.read()
    return html


def getList(regex, text):
    arr = []
    res = re.findall(regex, text)
    if res:
        for r in res:
            arr.append(r)
    return arr


def getMatch(regex, text):
    res = re.findall(regex, text)
    if res:
        return res[0]
    return ""


def clearTag(text):
    p = re.compile(u'<[^>]+>')
    retval = p.sub("", text)
    return retval


html = baidu_search('天下无贼')
content = str(html, 'utf-8', 'ignore')

arrList = getList(u"<table.*?class=\"result\".*?>.*?<\/a>", content)
for item in arrList:
    regex = u"<h3.*?class=\"t\".*?><a.*?href=\"(.*?)\".*?>(.*?)<\/a>"
    link = getMatch(regex, item)
    url = link[0]
    title = clearTag(link[1]).encode('utf8')
    # print(url
    print(title)
