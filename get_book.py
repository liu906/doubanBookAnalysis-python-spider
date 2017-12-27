import requests
import urllib
import re
import threading
from bs4 import *
import socket
import time
import csv


authors = ['https://book.douban.com/author/1071735/','https://book.douban.com/author/4514938/']
books = ['5431784', '26986954', '4820710', '25967870', '26279019']
def get_books():
    
    global books

    #从你的浏览器控制台复制出http报文的header信息
    header = {'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    for i in range(0,40,20):
        url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start='+str(i)+'&type=T'
        #print(url)
        #发送一个http请求，读出网页内容存到html
        req = urllib.request.Request(url,headers=header)
        html = urllib.request.urlopen(req).read()
        time.sleep(3)
        #网页里有中文，需要decode
        html.decode('utf-8','ignore')

        soup = BeautifulSoup(html,'lxml')


        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if re.match(r'https://book.douban.com/subject/[0-9]*/$',href):
                bookID = re.search(r'https://book.douban.com/subject/([0-9]*)/$',href).group(1)
                #print(href)
                books.append(bookID)
    return list(set(books))

def search_book():
    global books
    
    for counter,book in enumerate(books):
        url = 'https://book.douban.com/subject/'+book+'/'
        header = {'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
        time.sleep(2)
        req = urllib.request.Request(url,headers=header)
        with urllib.request.urlopen(req,timeout=30) as html:
            html = html.read()
            soup = BeautifulSoup(html,'lxml')
            recBooks = soup.find(id='db-rec-section').find_all('dd')
            for item in recBooks:
                bookLink = item.a.get('href')
                bookID = re.search(r'https://book.douban.com/subject/(.*)/',bookLink).group(1)
                print(bookID)
                if bookID not in books:
                    out = open('book_test.txt', 'a')
                    books.append(bookID)
                    out.write(bookID+'\n')
                    out.close()
                    #csv_writer = csv.writer(out, dialect='excel')
                    #csv_writer.writerow(bookID)
        if counter == 100:
            break
            
if __name__=='__main__':
    search_book()
    print(books)
