# -*- coding: utf-8 -*-
"""
Created on Sat May 12 11:05:00 2018

@author: Anan
"""

from bs4 import BeautifulSoup 
from urllib import request
import re
import csv
import time
import random
import pickle

def get_movie_url(movie_id):
    return "https://movie.douban.com/subject/{}/".format(movie_id)

def get_soup(url):
    res = request.urlopen(url)
    html = res.read().decode('utf-8')
    return BeautifulSoup(html,'html.parser')

def get_movie_info(soup):
    movie_name = soup.find('span', {'property': 'v:itemreviewed'}).get_text()
    year = soup.find('span', {'class': 'year'}).get_text().replace('(','').replace(')','')
    return movie_name,year

def get_comment_url(movie_id):
    return "https://movie.douban.com/subject/{}/comments".format(movie_id)

def get_second_page_comment_url(movie_id):
    return "https://movie.douban.com/subject/{}/comments?start=20&limit=20&sort=new_score&status=P&percent_type=".format(movie_id)



def get_movie_comments(soup):
    comment = []
    for c in soup.find_all('div', {'class': 'comment'}):
        try:
            content = c.find_all('p')[-1].text.strip()
            star = c.find('span', {'class': re.compile('^allstar')})['class'][0][-2]
            comment.append([content,star])
        except TypeError as e:
            print(e)
            continue
    return comment  

def get_complete_info(movie_id,movie_info, comments):
    movie_name, movie_year= movie_info
    return [(movie_id,movie_name, movie_year, c, s) for c, s in comments]

def write_the_data(complete_info):
    with open('douban_movie_comments.csv','a', newline='',encoding='gb18030') as file:
        writer=csv.writer(file)
        for entry in complete_info:
            writer.writerow(entry)
    print(complete_info[1][1],'comments wrote successfully!')

def random_sleep():
    random_sleep_time = random.randint(80, 200) / 10
    time.sleep(random_sleep_time)
       
def read_all_movie_id(filename):
    with open(filename, "rb") as fp:
           b = pickle.load(fp)
    return b

all_movie_id = read_all_movie_id("all_movie_id.txt")

def main(all_movie_id):
    with open('douban_movie_comments.csv','a', newline='') as file:
        writer=csv.writer(file)
        writer.writerow(['id', 'name', 'year', 'comment', 'star'])
    for id in all_movie_id:
        try:
            random_sleep()
            url_movie = get_movie_url(id)
            url_comment = get_comment_url(id)
            url_second_page_comment = get_second_page_comment_url(id)
            soup_movie = get_soup(url_movie)
            random_sleep()
            soup_comment = get_soup(url_comment)
            random_sleep()
            soup_comment_second_page = get_soup(url_second_page_comment)
            movie_info = get_movie_info(soup_movie)
            comments = get_movie_comments(soup_comment) + get_movie_comments(soup_comment_second_page)
            movie_complete_info = get_complete_info(id,movie_info, comments)
            write_the_data(movie_complete_info)
        except Exception as e:
            print(e)
            break
        

if __name__ == '__main__':
    main(all_movie_id)


