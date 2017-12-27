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
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
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
    
    #header = {'Host':'book.douban.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    header = {'Host': 'book.douban.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Cookie': 'bid=9-MVpTyNO1o; __utma=30149280.1544947207.1513732889.1514340780.1514359852.7; __utmz=30149280.1513732889.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_id.100001.3ac3=bab8cd32029ce905.1514213119.6.1514362223.1514342687.; __utma=81379588.1915505992.1514213121.1514340780.1514359852.6; __utmz=81379588.1514213121.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=O6dw9gVgeI3ahpyZZQK34CnjY6ut4lCb; viewed="4313213_5980585_7175434_6966737_10794370_5423775_25862578_1046265_6781800_1008074"; _vwo_uuid_v2=AF4F735B9F789D3706FCDEDAA90768C0|30f64568ffee308c04b921eb3e7e6dfd; gr_user_id=4351fb4f-6a81-4bb9-957a-3e662d8c5061; ll="108293"; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1514359837%2C%22https%3A%2F%2Fwww.douban.com%2Faccounts%2Flogin%3Fredir%3Dhttps%253A%252F%252Fbook.douban.com%252Ftag%252F%2525E5%2525B0%25258F%2525E8%2525AF%2525B4%253Fstart%253D0%2526type%253DT%22%5D; ap=1; ct=y; ps=y; dbcl2="132197651:SCOhpOVGLQM"; ck=ZDrx; _pk_ses.100001.3ac3=*; __utmb=30149280.8.10.1514359852; __utmc=30149280; __utmb=81379588.8.10.1514359852; __utmc=81379588; push_noty_num=0; push_doumail_num=0; __utmt_douban=1; __utmt=1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=d070604a-60d4-4aba-968a-f374557fe3ea; gr_cs1_d070604a-60d4-4aba-968a-f374557fe3ea=user_id%3A1',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': 1,
'Cache-Control': 'max-age=0'}
    
    for item in authors:
        url = 'https://book.douban.com/author/'+str(item.split()[0])+'/'
        print('url :',url)
        
        time.sleep(3)
        #print(req)
        try:
            req = urllib.request.Request(url,headers=header)
            html = urllib.request.urlopen(req,timeout=10).read()
            soup = BeautifulSoup(html,'lxml')
            name = soup.find(id='content').find('h1')
            if name =='':
                print('假网页，哼')
                continue
            print('爬到了真的网页')
            name = name.text
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
            out.close()
        except:
            print('there is an exception')
            continue
    authors.close()
    

if __name__=='__main__':
    get_author()
