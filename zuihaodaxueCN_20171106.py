# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def getHTML(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res.text
    except:
        return ''
    
def parse_ranking(url,ulist):
    html = getHTML(url)
    soup = BeautifulSoup(html,'html.parser')
    for tr in soup.tbody('tr'):  #soup.find('tbody').children:
        num = tr('td')[0].getText()
        uni = tr('td')[1].getText()
        ctry = tr('td')[2].select('img')[0].get('title')
        scr = tr('td')[3].getText()
        ulist.append([num,uni,ctry,scr])

def parse_subject(html,udict):
    soup = BeautifulSoup(html,'html.parser')
    divs = soup.select('div[class="col-lg-12 col-md-12 col-sm-12 col-xs-12"]')[2:]
    for div in divs:
        for a in div.select('a'):
            ulist = []
            sub = a.getText()
            href = 'http://www.zuihaodaxue.cn/' + a.get('href')
            parse_ranking(href,ulist)
            udict[sub] = ulist

def main():
    udict = {}
    url_subject = 'http://www.zuihaodaxue.cn/arwu_subject_rankings.html'    
    html = getHTML(url_subject)
    parse_subject(html,udict)   
    try:
        inquiry = input('Subject: ')
        print('{0:^5}\t{1:{4}<12}\t{2:^10}\t{3:^10}'.format('排名','学校','国家','总分',chr(12288)))
        if inquiry in udict.keys():
            for line in udict[inquiry]:
                print('{0:^5}\t{1:{4}<10}\t{2:^10}\t{3:^10}'.format(line[0],line[1],line[2],line[3],chr(12288)))
    except:
        return ''

main()






