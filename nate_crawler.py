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
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.category_list = []

class Category:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.article_list = []

class Article:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.bple_list = []

class Bple:
    def __init__(self, contents):
        self.contents = contents

class CrawlData:
    def crawl_data(self, driver, category):
        driver.get(category.url)
        source = driver.page_source
        tree = lh.fromstring(source)
        url_list = list(map(lambda x:x.get('href'), tree.cssselect('.rk_list li a')))

        for url in url_list:
            driver.get(url)
            title = ''
            bple_contents = []
            try:
                WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'news_cmt'))
                )
                source = driver.page_source
                a_tree = lh.fromstring(source)
                title = a_tree.cssselect('#artcTitle')[0].text_content()
                bple_contents = list(map(lambda x:x.text_content(), a_tree.cssselect('.reply:not(.others) > dl > dd.userText > a:nth-of-type(1)')))
            except:
                pass
            finally:
                article = new Article(title, url)
                for content in bple_contents:
                    article.append(new Bple(content))
                category.article_list.append(article)

class NateCrawler:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.site = new Site('nate', 'http://m.nate.com')
        self.site.category_list.fromlist([
                new Category('sisa', 'http://m.news.nate.com/rank/list?mid=m0001&section=sisa&rmode=interest'),
                new Category('ent', 'http://m.news.nate.com/rank/list?mid=e0001&section=ent&rmode=interest'),
                new Category('spo', 'http://m.news.nate.com/rank/list?mid=s0001&section=spo&rmode=interest')
        ])

    def run(self):
        for category in self.site.category_list:
            cd = CrawlData()
            cd.crawl_data(self.driver, category)
       
       '''
        for cd in self.data_list:
            c = 0
            for bple_list in cd.url_to_bple.viewvalues():
                for bple in bple_list:
                    print '[' + str(c) + ']: ' + bple
                c = c+1
        '''

    def __del__(self):
        self.driver.quit()
    
if __name__ == "__main__":
    crawler = NateCrawler()
    crawler.run()