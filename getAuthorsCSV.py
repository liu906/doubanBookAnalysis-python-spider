import requests
import urllib
import re
import threading
from bs4 import *
import socket
import time
import csv

#返回一位作家评价最高的前五本书[书名，评分，评价人数]
def get_booklist(author_id):
    booklist = []
    url = 'https://book.douban.com/author/'+str(author_id)+'/books?sortby=collect&format=pic'
    header = {'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    req = urllib.request.Request(url,headers=header)   
    with urllib.request.urlopen(req,timeout=30) as html:
        html = html.read()
        soup = BeautifulSoup(html,'lxml')
        items = soup.find(class_='grid_view').find('ul').find_all('dd')
        for counter,item in enumerate(items):
            book_name = item.find('h6').a.text
            star = item.find(class_='star clearfix').find_all('span')[1].text
            evStr = item.find(class_='star clearfix').find_all('span')[2].text
            evNum = re.search(u'([0-9]*)人评价'.encode('utf-8'),evStr.encode('utf-8')).group(1).decode('utf-8')
            
            if star!='' :
                book = (book_name,star,evNum)
                #print(book_name,star,evNum)
                booklist.append(book)
            if counter==5 :
                break
                
        return booklist

def get_author():
    authors = open('author_id.txt','r')
    #authors = set(authors)
    header = {'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    for item in authors:
        url = item.split()[0]
        print('url :',url)
        req = urllib.request.Request(url,headers=header)

        with urllib.request.urlopen(req,timeout=30) as html:
            html = html.read()
            soup = BeautifulSoup(html,'lxml')
            name = soup.find(id='content').h1.text
            info = soup.find(class_='info').ul.find_all('li')
            gender = re.search(u'男|女'.encode('utf-8'),info[0].text.encode('utf-8')).group().decode('utf-8')
            birthday = re.search(r'[0-9].*',info[1].text).group()
            country = re.search(u'(.*):(.*)'.encode('utf-8'),info[2].text.encode('utf-8'),re.S).group(2).decode('utf-8')
            country = country.strip()
    
            author_id = re.search(r'(.*)author/(.*)/',url).group(2)
            
            
            out = open('author.csv', 'a', newline='')
            csv_writer = csv.writer(out, dialect='excel')
            
            print(author_id,name,gender,birthday,country,get_booklist(author_id))
            
            csv_writer.writerow([author_id,name,gender,birthday,country,get_booklist(author_id)])
            #out.close()

if __name__=='__main__':
    get_author()
