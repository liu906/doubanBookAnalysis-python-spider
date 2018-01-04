import requests
import urllib
import re
import threading
from bs4 import *
import socket
import time
import csv
from urllib import parse





def get_books(label):
    out = open(parse.unquote(label)+'.txt', 'w')
    #从你的浏览器控制台复制出http报文的header信息
    header = {'Host': 'book.douban.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Cookie': 'bid=9-MVpTyNO1o; __utma=30149280.1544947207.1513732889.1514340780.1514359852.7; __utmz=30149280.1513732889.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_id.100001.3ac3=bab8cd32029ce905.1514213119.6.1514362223.1514342687.; __utma=81379588.1915505992.1514213121.1514340780.1514359852.6; __utmz=81379588.1514213121.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=O6dw9gVgeI3ahpyZZQK34CnjY6ut4lCb; viewed="4313213_5980585_7175434_6966737_10794370_5423775_25862578_1046265_6781800_1008074"; _vwo_uuid_v2=AF4F735B9F789D3706FCDEDAA90768C0|30f64568ffee308c04b921eb3e7e6dfd; gr_user_id=4351fb4f-6a81-4bb9-957a-3e662d8c5061; ll="108293"; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1514359837%2C%22https%3A%2F%2Fwww.douban.com%2Faccounts%2Flogin%3Fredir%3Dhttps%253A%252F%252Fbook.douban.com%252Ftag%252F%2525E5%2525B0%25258F%2525E8%2525AF%2525B4%253Fstart%253D0%2526type%253DT%22%5D; ap=1; ct=y; ps=y; dbcl2="132197651:SCOhpOVGLQM"; ck=ZDrx; _pk_ses.100001.3ac3=*; __utmb=30149280.8.10.1514359852; __utmc=30149280; __utmb=81379588.8.10.1514359852; __utmc=81379588; push_noty_num=0; push_doumail_num=0; __utmt_douban=1; __utmt=1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=d070604a-60d4-4aba-968a-f374557fe3ea; gr_cs1_d070604a-60d4-4aba-968a-f374557fe3ea=user_id%3A1',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': 1,
'Cache-Control': 'max-age=0'}

    for i in range(0,800,20):
        try:
            url = 'https://book.douban.com/tag/' + label +'?start='+str(i)+'&type=T'
            print(url)
            #发送一个http请求，读出网页内容存到html
            req = urllib.request.Request(url,headers=header)
            html = urllib.request.urlopen(req).read()
            time.sleep(1)
            #网页里有中文，需要decode
            html.decode('utf-8','ignore')

            soup = BeautifulSoup(html,'lxml')

            links = soup.find_all('h2')
            for link in links:
                link = link.find('a')
                href = link.get('href')
                if re.match(r'https://book.douban.com/subject/[0-9]*/$',href):
                    bookID = re.search(r'https://book.douban.com/subject/([0-9]*)/$',href).group(1)
                    print(bookID)
                    out.write(bookID+'\n')
        except:
            print('爬取该列表页面出错')
    out.close()



            
if __name__=='__main__':

    
    threads = []

    #小说 外国文学 漫画 武侠 哲学 心理学 儿童文学 魔幻 悬疑 名著
    #labels = ['%E5%B0%8F%E8%AF%B4','%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6','%E6%BC%AB%E7%94%BB','%E6%AD%A6%E4%BE%A0','%E5%93%B2%E5%AD%A6','%E5%BF%83%E7%90%86%E5%AD%A6','%E5%84%BF%E7%AB%A5%E6%96%87%E5%AD%A6','%E9%AD%94%E5%B9%BB','%E6%82%AC%E7%96%91','%E5%90%8D%E8%91%97']
    #拉美文学 美国 历史 杂文 当代文学
    labels = ['%E6%8B%89%E7%BE%8E%E6%96%87%E5%AD%A6','%E7%BE%8E%E5%9B%BD','%E5%8E%86%E5%8F%B2','%E6%9D%82%E6%96%87','%E5%BD%93%E4%BB%A3%E6%96%87%E5%AD%A6']
    for label in labels:
        th = threading.Thread(target=get_books,args=(label,))
        threads.append(th)

    for th in threads:
        th.start()
        time.sleep(1)
