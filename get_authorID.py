import requests
import urllib
import re
import threading
from bs4 import *
import socket
import time
import csv

auther_ids = []

def book_page(book_id):
    global auther_ids
    url = 'https://book.douban.com/subject/'+str(book_id)+'/'
    #url just like https://book.douban.com/subject/27079142/
    header = {'User-Agent':'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    req = urllib.request.Request(url,headers=header)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html,'lxml')
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if re.match(r'https://book.douban.com/author/[0-9]*/',href):
            author_id = re.search(r'https://book.douban.com/author/(.*)/',href).group(1)
            if author_id not in auther_ids:
                author_id_txt = open('author_id.txt','a')
                author_id_txt.write(author_id+'\n')
                auther_ids.append(author_id)
                print(author_id)


if __name__=='__main__':
    books = open('book_test.txt')
    for item in books:
        book_page(item.split()[0])