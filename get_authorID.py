import requests
import urllib
import re
import threading
from bs4 import *
import socket
import time
import csv
from urllib import parse

author_ids = []

def get_books(label):
    global author_ids

    books = open(label+'.txt','r')
    for book_id in books:
        book_id = book_id.split()[0]
        book_page(label,book_id)


def book_page(label,book_id):

    global author_ids
    url = 'https://book.douban.com/subject/'+str(book_id)+'/'

    #url just like https://book.douban.com/subject/27079142/
    header = {'Host': 'book.douban.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

    try:
        req = urllib.request.Request(url,headers=header)
        #print('req successfully')
        html = urllib.request.urlopen(req).read()
        #print('html successfully')
        soup = BeautifulSoup(html,'lxml')
        #print('soup')
        links = soup.find_all('a')
        for link in links:
            #print('aaaaa')
            href = link.get('href')
            if re.match(r'https://book.douban.com/author/[0-9]*/',href):
                #print('bbbb')
                author_id = re.search(r'https://book.douban.com/author/(.*)/',href).group(1)
                if author_id not in author_ids:
                
                    author_id_txt = open('authorIDSecond.txt','a')
                
                    author_id_txt.write(author_id+'\n')
                 
                    author_id_txt.close()
                 
                    author_ids.append(author_id)
              
                    print(author_id)
                
                else :
                    print('已经有这个作者了')
                break

    except:
        print('连接错误')
        time.sleep(3)


if __name__=='__main__':


    threads = []
    #labels = ['%E5%B0%8F%E8%AF%B4','%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6','%E6%BC%AB%E7%94%BB','%E6%AD%A6%E4%BE%A0','%E5%93%B2%E5%AD%A6','%E5%BF%83%E7%90%86%E5%AD%A6','%E5%84%BF%E7%AB%A5%E6%96%87%E5%AD%A6','%E9%AD%94%E5%B9%BB','%E6%82%AC%E7%96%91','%E5%90%8D%E8%91%97']
    labels = ['%E6%8B%89%E7%BE%8E%E6%96%87%E5%AD%A6','%E7%BE%8E%E5%9B%BD','%E5%8E%86%E5%8F%B2','%E6%9D%82%E6%96%87','%E5%BD%93%E4%BB%A3%E6%96%87%E5%AD%A6']
    for label in labels:

        label = parse.unquote(label)
        print('label = ',label)
        th = threading.Thread(target=get_books,args=(label,))
        threads.append(th)
    for th in threads:
        th.start()
        time.sleep(1)