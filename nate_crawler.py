#!/usr/bin/env python

import time
from selenium import webdriver

class NateCrawler:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def getData(self, anchor):
        anchor.click()
        time.sleep(2)
        anchor_list = self.driver.find_elements_by_css_selector('.rollItem + div[style*=\"left: 0px\"] .ct1 li a')
        print 'length of anchor list = ' + str(len(anchor_list))

    def run(self):
        driver = self.driver
        driver.get('http://m.nate.com')
        time.sleep(2)
        driver.find_element_by_css_selector('.blockNavi .navTab li:nth-child(2) a').click()
        time.sleep(1)
        sisa_a = driver.find_element_by_css_selector('.tabNav li[data-btn=\"rank0\"] a')
        ent_a = driver.find_element_by_css_selector('.tabNav li[data-btn=\"rank1\"] a')
        spo_a = driver.find_element_by_css_selector('.tabNav li[data-btn=\"rank2\"] a')

        self.getData(sisa_a)

    
    def __del__(self):
        self.driver.quit()
    
if __name__ == "__main__":
    crawler = NateCrawler()
    crawler.run()