import csv
import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']  

def author_avg_popularity(author):
    author = author[5][1:-1]
    arr = re.findall(r"\(.+?,.+?,.+?\)",author)
    sum = 0
    try :
        for book in arr:
            item = book.split(',')
            num = int(re.search(r'([^0-9]+)([0-9]*)([^0-9]+)',item[2]).group(2))  
            sum += num
        avg = sum/len(arr)
        return avg
    except:
        return 0
  
def rank_by_pop():
    rank = []
    handle = open('author.csv','r')
    csv_reader = csv.reader(handle)
    for author in csv_reader:
        name = author[1]
        #print(name)
        avg = author_avg_popularity(author)
        if avg == 0:
            continue
        rank.append([name,avg])
    rank = sorted(rank, key=lambda rank:rank[1])    
    return rank

def Biggset10Author(rank):
    top10 = rank[-10:]
    return top10

def Smallest10Author(rank):
    rank = rank_by_pop()
    top10 = rank[0:10]
    return top10

def draw_top10(top10):
    top10.reverse()
    name_list = []
    #for author in top10:
    #    name_list.append(author[0])
    name_list = ['安东尼·埃克苏佩里','东野圭吾','卡勒德·胡赛尼','郭敬明','村上春树','韩寒','J·K·罗琳','刘慈欣','林少华','余华']
    pop = []
    for i,item in enumerate(top10):
        name_list.append(top10[i][0])
        pop.append(top10[i][1])
        
    rects = plt.bar(range(0,10),pop,width=0.3,align="center",color=('#800000','#B22222','#A52A2A','#CD5C5C','#F08080','#BC8F8F','#FF6347','#E9967A','#FFEFD5','#EEE8AA'))  
    plt.xticks(range(len(pop)),name_list,rotation=0,fontsize=16)
    plt.title('最受欢迎作者TOP10',fontsize=18)
    for i,rect in enumerate(rects):
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height, "%s" % int(height))
    
    
    plt.show()  
    #plt.savefig('C:\Users\liuxu\Desktop\liu906.github.io\top10.png')

def author_avg_grade(author):
    author = author[5][1:-1]
    arr = re.findall(r"\(.+?,.+?,.+?\)",author)
    sum = 0
    length = len(arr)
    try :
        for book in arr:
            item = book.split(',')
            num = float(re.search(r'([^0-9]+)([0-9][^0-9][0-9])([^0-9]+)',item[1]).group(2))
            if num>=10 or num <= 2:
                length = length -1
            sum += num
        avg = sum/length  
        return avg 
    except:
        return 0 


def rank_by_grade():
    rank = []
    handle = open('author.csv','r')
    csv_reader = csv.reader(handle)
    for author in csv_reader:
        name = author[1]
        country = author[2]
        gender = author[4]
        #print(name)
        avg = author_avg_grade(author)
        if avg == 0:
            continue
        rank.append([name,avg,country,gender])
        
    rank = sorted(rank, key=lambda rank:rank[1])
    return rank

def highest_grade(rank):

    top30 = rank[-30:]
    handle = open('HighestGradeTop30.csv','w')
    csv_writer = csv.writer(handle, dialect='excel')
    for item in top30:
        #handle.write(item[0],item[1],item[2],item[3])
  
        csv_writer.writerow(item)
    handle.close()
    return top30


def draw_highset_grade(top30):

    male = 0
    female = 0
    for item in top30:
        if item[2]=='男':
            male = male + 1
        else :
            female = female + 1 

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = '男', '女'
    sizes = [male,female]
    explode = (0,0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90,colors=('#76C0C3','#E8916F'))
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('评分最高的30位作家男女比例')

    plt.show()

def foreignAuthor(country):
    #豆瓣用户最喜爱的美国、加拿大、英国、德国、俄国、日本、台湾作家
    handle = open('author.csv','r')
    csv_reader = csv.reader(handle)

    pop_max = 0
    grade_max = 0
    grade_name_pop = 0
    pop_name_grade = 0
    pop_name = ''
    grade_name = ''
    for author in csv_reader:
        if author[4]==country:
            grade_avg = author_avg_grade(author)
            pop_avg = author_avg_popularity(author)
            if grade_avg > grade_max:
                grade_max = grade_avg
                grade_name = author[1]
                grade_name_pop = author_avg_popularity(author)

            if pop_avg > pop_max:
                pop_max = pop_avg
                pop_name = author[1]
                pop_name_grade = author_avg_grade(author)
    return [country,pop_name,round(pop_max,2),round(pop_name_grade,2),grade_name,round(grade_name_pop,2),round(grade_max,2)]

def foreignAuthor_write_csv():
    country_labels = ['英国','美国','加拿大','德国','俄罗斯','日本','中国台湾','中国香港']
    out = open('analysis_result/foreignAuthor.csv', 'a', newline='')
    csv_writer = csv.writer(out, dialect='excel')
    csv_writer.writerow(['国家','最受欢迎作者','平均每部作品评价人次','平均作品得分','评分最高作者','平均每部作品的评价人次','平均作品得分'])
    for country in country_labels:
        csv_writer.writerow(foreignAuthor(country))
        print(foreignAuthor(country))

def author_range(author):
    author = author[5][1:-1]
    arr = re.findall(r"\(.+?,.+?,.+?\)",author)
    max = 0
    min = 10
    try :
        for book in arr:
            item = book.split(',')
            num = float(re.search(r'([^0-9]+)([0-9][^0-9][0-9])([^0-9]+)',item[1]).group(2))
            if num>max :
                max = num
            if num<min :
                min = num
        return max - min
    except:
        return 0     

def  MostUnstableAuthor():
    rank = []
    handle = open('author.csv','r')
    csv_reader = csv.reader(handle)
    for author in csv_reader:
        name = author[1]
        #print(name)
        a_range = author_range(author)
        if a_range == 0:
            continue
        rank.append([name,a_range])
    rank = sorted(rank, key=lambda rank:rank[1])   
    print(rank) 
    return rank



if __name__=='__main__':

    #draw_top10(MostPopularAuthor())
    #draw_highset_grade(highest_grade(rank_by_grade()))
    #foreignAuthor_write_csv()

    #draw_top10(Biggset10Author(MostUnstableAuthor()))
    #rank_by_pop
    draw_top10(Biggset10Author(rank_by_pop()))

