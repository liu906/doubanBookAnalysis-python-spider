import requests
import urllib
import re
import threading
from bs4 import *
import socket
import time
import csv


authors = []
books = []
def get_books():
    
    global books
    #从你的浏览器控制台复制出http报文的header信息
    header = {'Host': 'book.douban.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Cookie': 'bid=9-MVpTyNO1o; __utma=30149280.1544947207.1513732889.1514340780.1514359852.7; __utmz=30149280.1513732889.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_id.100001.3ac3=bab8cd32029ce905.1514213119.6.1514362223.1514342687.; __utma=81379588.1915505992.1514213121.1514340780.1514359852.6; __utmz=81379588.1514213121.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=O6dw9gVgeI3ahpyZZQK34CnjY6ut4lCb; viewed="4313213_5980585_7175434_6966737_10794370_5423775_25862578_1046265_6781800_1008074"; _vwo_uuid_v2=AF4F735B9F789D3706FCDEDAA90768C0|30f64568ffee308c04b921eb3e7e6dfd; gr_user_id=4351fb4f-6a81-4bb9-957a-3e662d8c5061; ll="108293"; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1514359837%2C%22https%3A%2F%2Fwww.douban.com%2Faccounts%2Flogin%3Fredir%3Dhttps%253A%252F%252Fbook.douban.com%252Ftag%252F%2525E5%2525B0%25258F%2525E8%2525AF%2525B4%253Fstart%253D0%2526type%253DT%22%5D; ap=1; ct=y; ps=y; dbcl2="132197651:SCOhpOVGLQM"; ck=ZDrx; _pk_ses.100001.3ac3=*; __utmb=30149280.8.10.1514359852; __utmc=30149280; __utmb=81379588.8.10.1514359852; __utmc=81379588; push_noty_num=0; push_doumail_num=0; __utmt_douban=1; __utmt=1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=d070604a-60d4-4aba-968a-f374557fe3ea; gr_cs1_d070604a-60d4-4aba-968a-f374557fe3ea=user_id%3A1',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': 1,
'Cache-Control': 'max-age=0'}
    
    '''
    header = {'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    '''
    for i in range(320,800,20):
        try:
            url = 'https://book.douban.com/tag/%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6?start='+str(i)+'&type=T'
            #print(url)
            #发送一个http请求，读出网页内容存到html
            req = urllib.request.Request(url,headers=header)
            html = urllib.request.urlopen(req).read()
            time.sleep(1)
            #网页里有中文，需要decode
            html.decode('utf-8','ignore')

            soup = BeautifulSoup(html,'lxml')


            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if re.match(r'https://book.douban.com/subject/[0-9]*/$',href):
                    bookID = re.search(r'https://book.douban.com/subject/([0-9]*)/$',href).group(1)
                    if bookID not in books:
                        print(bookID)
                        books.append(bookID)
        except:
            print('爬取该列表页面出错')
        

def search_book():
    global books
    for counter,book in enumerate(books):
        url = 'https://book.douban.com/subject/'+book+'/'
        header = {'Host': 'book.douban.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Cookie': 'bid=9-MVpTyNO1o; __utma=30149280.1544947207.1513732889.1514340780.1514359852.7; __utmz=30149280.1513732889.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_id.100001.3ac3=bab8cd32029ce905.1514213119.6.1514362223.1514342687.; __utma=81379588.1915505992.1514213121.1514340780.1514359852.6; __utmz=81379588.1514213121.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=O6dw9gVgeI3ahpyZZQK34CnjY6ut4lCb; viewed="4313213_5980585_7175434_6966737_10794370_5423775_25862578_1046265_6781800_1008074"; _vwo_uuid_v2=AF4F735B9F789D3706FCDEDAA90768C0|30f64568ffee308c04b921eb3e7e6dfd; gr_user_id=4351fb4f-6a81-4bb9-957a-3e662d8c5061; ll="108293"; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1514359837%2C%22https%3A%2F%2Fwww.douban.com%2Faccounts%2Flogin%3Fredir%3Dhttps%253A%252F%252Fbook.douban.com%252Ftag%252F%2525E5%2525B0%25258F%2525E8%2525AF%2525B4%253Fstart%253D0%2526type%253DT%22%5D; ap=1; ct=y; ps=y; dbcl2="132197651:SCOhpOVGLQM"; ck=ZDrx; _pk_ses.100001.3ac3=*; __utmb=30149280.8.10.1514359852; __utmc=30149280; __utmb=81379588.8.10.1514359852; __utmc=81379588; push_noty_num=0; push_doumail_num=0; __utmt_douban=1; __utmt=1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=d070604a-60d4-4aba-968a-f374557fe3ea; gr_cs1_d070604a-60d4-4aba-968a-f374557fe3ea=user_id%3A1',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': 1,
'Cache-Control': 'max-age=0'}
        
        
        
        try:
            req = urllib.request.Request(url,headers=header)
            html = urllib.request.urlopen(req,timeout=30).read()
            time.sleep(4)
            soup = BeautifulSoup(html,'lxml')
            recBooks = soup.find(id='db-rec-section').find_all('dd')
            for item in recBooks:
                bookLink = item.a.get('href')
                bookID = re.search(r'https://book.douban.com/subject/(.*)/',bookLink).group(1)
                
                if bookID not in books:
                    print(bookID)
                    books.append(bookID)
                if counter == 100:
                    break
        except:
            if counter == 100:
                break
            print('search_book error')

def write_book():
    out = open('book_waiguowenxue.txt', 'a')
    for item in books:
        out.write(item+'\n')
    out.close()
            
if __name__=='__main__':
    get_books()
    write_book()