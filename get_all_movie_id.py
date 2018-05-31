# -*- coding: utf-8 -*-
"""
Created on Sat May 12 11:05:00 2018

@author: Anan
"""


from bs4 import BeautifulSoup 
from urllib import request
import re
import time
import random
import pickle
import urllib.error


def random_sleep():
    random_sleep_time = random.randint(80, 200) / 10
    time.sleep(random_sleep_time)
       
def get_movie_url(movie_id):
    return "https://movie.douban.com/subject/{}/".format(movie_id)

def get_soup(url):
    res = request.urlopen(url)
    html = res.read().decode('utf-8')
    return BeautifulSoup(html,'html.parser')    
    
def get_recommends_list(soup):
    recommends = soup.find('div', {'class': 'recommendations-bd'})
    names = [a['alt'] for a in recommends.find_all('img')]
    ids = [re.search('subject/(.*)/', a['href']).group(1)
             for ii, a in enumerate(recommends.find_all('a'))
             if ii % 2 == 0]
    return list(ids)


def read_all_movie_id(filename):
    with open(filename, "rb") as fp:
           b = pickle.load(fp)
    return b


def get_all_movie_id(first_movie_id,num):
    visited = read_all_movie_id("all_movie_id.txt")
    #visited = set()
    unvisited = []
    unvisited.append(first_movie_id)
    while len(unvisited) > 0:
        if len(visited) >= num:break
        try:
            need_visited = unvisited.pop(0)
            random_sleep()
            new_add_visited = get_recommends_list(get_soup(get_movie_url(need_visited)))
            for id in new_add_visited:visited.add(id)
            unvisited += new_add_visited
        #except urllib.error.HTTPError as e:
        except Exception as e:
            #print(e)
            break
    return visited
        
        
def save_all_movie_id(visited):
    with open("all_movie_id.txt", "wb") as fp:
        pickle.dump(visited, fp)
        
start = time.clock()      
visited = get_all_movie_id(27196380,1500)
save_all_movie_id(visited)
run_time = time.clock() - start