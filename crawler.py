
import requests
import time
import urllib
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from multiprocessing import Pool
from lxml.html import fromstring
import os, sys
import wget
 
n = 1
def search(url):
 
    browser = webdriver.Chrome('chromedriver')#웹 드라이버 사용
    
    browser.get(url)#URL을 불러옴
    time.sleep(0.5)
    element = browser.find_element_by_tag_name("body")#body tag를 찾는다
  
    for i in range(40):
        element.send_keys(Keys.PAGE_DOWN)#페이지를 아래로 스크롤한다
        time.sleep(0.1)
    browser.find_element_by_id("smb").click()#smb(버튼의 id)를 찾으면 클릭

    for i in range(10):
        element.send_keys(Keys.PAGE_DOWN)#페이지 아래로 스크롤
        time.sleep(0.2)
 
    time.sleep(1)
 
    source = browser.page_source#브라우저 소스를 강져옴
    browser.close()#브라우저 닫음
 
    return source

def download_image(link):
    global n


    headers = {"User-Agent": ua.random} #권한 설정
 
    
    try:
        r = requests.get("https://www.google.com" + link.get("href"), headers=headers) #권한 부여, 요청 (href = hypertext reference)
    except:
        print("Cannot get link.")
    
    title = fromstring(r.content).findtext(".//title") #string에서 .//title 텍스트를 찾는다
    link_url = title.split(" ")[-1]#찾은 문자열 정리
    print (link_url)
    
    if link_url.find(".jpg")==len(link_url)-4: #찾은 문자열에서 마지막 네 자리가 .jpg인것만 다운로드

        wget.download(link_url, str(os.getcwd()) + "/" + query+"/"+str(n)+".jpg") #query라는 변수를 폴더명으로 하고, working directory에 저장한다
    n=n+1




sys.setrecursionlimit(100000000) # 시스템 시간 설정

query = input(u'검색어 : ')
count = int(input('다운로드 개수 : '))
url = "https://www.google.com/search?as_st=y&tbs=isz%3Alt%2Cislt%3Asvga%2Citp%3Aphoto%2Cift%3Ajpg&tbm=isch&sa=1&ei=H_-KW6GSHImGoAS3z4DYCA&q=" +query+"&oq="+query+"&gs_l=img.3..0l10.19389.19389.0.21095.1.1.0.0.0.0.113.113.0j1.1.0....0...1c.1.64.img..0.1.111....0.QpKT5Qs8Kdo"
print (url)
source = search(url) #위에 만든 함수 실행


page_text = source.encode('utf-8').decode('ascii', 'ignore') #받아온 텍스트 변환 (안해도 됨)
soup = BeautifulSoup(page_text, "html.parser") #html형식 파싱
ua = UserAgent() #전역변수로 download_image에서 쓰임



if not os.path.isdir(query): #작업 환경 설정
    os.makedirs(query) #query 변수명으로 작업 폴더 생성

links = soup.find_all("a", class_="rg_l") #이미지 다운을 위한 링크를html에서 찾는다
for l in links[0:count]:
    try:
        download_image(l)
        print("success")
    except:
        print("fail")

        pass
