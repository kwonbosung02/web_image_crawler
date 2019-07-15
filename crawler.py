import requests 
import time
import urllib
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from multiprocessing import pool
from lxml.html import fromstring 
import os, sys
import time 
import wget

n = 1


def search(url):
    browser = webdriver.Chrome('chromedriver')
    browser.get(url)
    time.sleep(1)
    element = browser.find_element_by_tag_name("body")

    for i in range(40):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    
    browser.find_element_by_id("smb").click()

    for i in range(20):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    
    time.sleep(0.5)

    source = browser.page_source
    browser.close()
    #print(source)
    return source




def download(link):
    global n
    headers = {"User-Agent": ua.random}

    try:
        r = requests.get("https://www.google.com"+link.get("href"), headers=headers)
    
    except:
        print("error")

    title = fromstring(r.content).findtext(".//title")
    link_url = title.split(" ")[-1]
    print(link_url)

    if link_url.find(".jpg")==len(link_url)-4:
        print(link_url)
        wget.download(link_url,str(os.getcwd()) + "/" + query + "/" + str(n) + ".jpg")
    n = n + 1
sys.setrecursionlimit(100000000)

query = input(u'검색어 : ')
count= int(input("다운로드 개수 : "))
url ="https://www.google.com/search?as_st=y&tbs=isz%3Alt%2Cislt%3Asvga%2Citp%3Aphoto%2Cift%3Ajpg&tbm=isch&sa=1&ei=H_-KW6GSHImGoAS3z4DYCA&q=" +query+"&oq="+query+"&gs_l=img.3..0l10.19389.19389.0.21095.1.1.0.0.0.0.113.113.0j1.1.0....0...1c.1.64.img..0.1.111....0.QpKT5Qs8Kdo"

print(url)

source = search(url)

page_text = source.encode('utf-8').decode('ascii', 'ignore')
soup = BeautifulSoup(page_text,"html.parser")
ua = UserAgent()



if __name__ == "__main__":
    if not os.path.isdir(query):
        os.makedirs(query)

    links = soup.find_all("a", class_="rg_l")
    print(links)
    for li in links[0:count]:
        try:
            print(li + "다운로드시작")
            download(li)
            print("OK")
        except:
            print("에러")
            pass