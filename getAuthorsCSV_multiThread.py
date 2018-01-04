import requests
import urllib
import re
import threading
from bs4 import *
import socket
import time
import csv
import threading

#返回一位作家评价最高的前五本书[书名，评分，评价人数]
def get_booklist(author_id):
    booklist = []
    url = 'https://book.douban.com/author/'+str(author_id)+'/books?sortby=collect&format=pic'
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    req = urllib.request.Request(url,headers=header)
    #print('req successfully')  
    try: 
        html = urllib.request.urlopen(req,timeout=30).read()
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
    except:
        print("get book list error")
        return booklist

def get_author(author_id):
    #authors = open('author_id.txt','r')
    
    #header = {'Host':'book.douban.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    header = {'Host': 'book.douban.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    
    #for item in authors:
    url = 'https://book.douban.com/author/'+str(author_id)+'/'
    print('url :',url)
        #print(req)
    try:
        req = urllib.request.Request(url,headers=header)
        html = urllib.request.urlopen(req,timeout=30).read()
        soup = BeautifulSoup(html,'lxml')
        name = soup.find(id='content').find('h1')
        if name =='':
            print('假网页，哼')
        #print('爬到了真的网页')
        name = name.text
        info = soup.find(class_='info').ul.find_all('li')
        #print('get info')
        gender = re.search(u'男|女'.encode('utf-8'),info[0].text.encode('utf-8')).group().decode('utf-8')
        #print('get gender',gender)
        birthday = re.search(r'[0-9].*',info[1].text).group()
        #print('get birthday',birthday)
        country = re.search(u'(.*):(.*)'.encode('utf-8'),info[2].text.encode('utf-8'),re.S).group(2).decode('utf-8')
        #print('get country',country)
        country = country.strip()


    
        author_id = re.search(r'(.*)author/(.*)/',url).group(2)
        
        #print('get author_id',author_id)
            
        out = open('authorSecond.csv', 'a', newline='')
        #print('open successfully')

        csv_writer = csv.writer(out, dialect='excel')
        #print('csv_writer successfully')

        

        csv_writer.writerow([author_id,name,gender,birthday,country,get_booklist(author_id)])
        print(author_id,name,gender,birthday,country,get_booklist(author_id))
        out.close()
    except:
        print('there is an exception')
        time.sleep(4)
    
    
if __name__=='__main__':

    threads = []
    authors = open('authorIDSecond.txt','r')
    for item in authors:
        author_id = str(item.split()[0])
        th = threading.Thread(target=get_author,args=(author_id,))
        threads.append(th)

    authors.close()

    for th in threads:
        th.start()
        time.sleep(1)

