#!/usr/bin/env python

import time
import lxml.html as lh
from collections import OrderedDict
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Site:
    def __init__(self, name, url, category_list):
        self.name = name
        self.url = url
        self.category_list = category_list

class Category:
    def __init__(self, name, article_list)
        self.name = name
        self.article_list = article_list

class Article:
    def __init__(self, title, url, bple_list):
        self.title = title
        self.url = url
        self.bple_list = bple_list

class Bple:
    def __init__(self, contents):
        self.contents = contents

class CrawlData:
    def __init__(self):
        self.title_to_url = OrderedDict()
        self.url_to_bple = OrderedDict()

    def crawl_data(self, driver, url):
        driver.get(url)
        source = driver.page_source
        #soup = BeautifulSoup(source)
        tree = lh.fromstring(source)
        title_list = list(map(lambda x:x.text_content(), tree.cssselect('.rk_list li a span')))
        url_list = list(map(lambda x:x.get('href'), tree.cssselect('.rk_list li a')))
        for t,u in zip(title_list, url_list):
            self.title_to_url[t] = u

        for url in url_list:
            driver.get(url)
            bple_list = []
            try:
                WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'news_cmt'))
                )
                source = driver.page_source
                #soup = BeautifulSoup(source)
                a_tree = lh.fromstring(source)
                #:not(.class) is not supported
                bple_list = list(map(lambda x:x.text_content(), a_tree.cssselect('.reply:not(.others) > dl > dd.userText > a:nth-of-type(1)')))
            except:
                pass
            finally:
                self.url_to_bple[url] = bple_list

class NateCrawler:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.main_links = ['http://m.news.nate.com/rank/list?mid=m0001&section=sisa&rmode=interest']
                #'http://m.news.nate.com/rank/list?mid=e0001&section=ent&rmode=interest',
                #'http://m.news.nate.com/rank/list?mid=s0001&section=spo&rmode=interest']
        self.data_list = []

    def run(self):
        for link in self.main_links:
            cd = CrawlData()
            cd.crawl_data(self.driver, link)
            self.data_list.append(cd)
        
        for cd in self.data_list:
            c = 0
            for bple_list in cd.url_to_bple.viewvalues():
                for bple in bple_list:
                    print '[' + str(c) + ']: ' + bple
                c = c+1

    def __del__(self):
        self.driver.quit()
    
if __name__ == "__main__":
    crawler = NateCrawler()
    crawler.run()