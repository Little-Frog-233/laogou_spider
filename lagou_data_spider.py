#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 17:16:26 2018

@author: little-frog
"""
import time
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq

path = 'chromedriver'
KEYWORD = '数据分析'
CITY = '上海'
path_save = '数据分析_上海.txt'
browser = webdriver.Chrome(path)
wait = WebDriverWait(browser,10)

###获取最大页码
def get_number():
    url = 'https://www.lagou.com/jobs/list_%s?city=%s'%(KEYWORD,CITY)
    all_pages = []
    try:
        browser.get(url)
        pages = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.pager_not_current')))
        for page in pages:
            all_pages.append(page.text)
        #browser.close()
        return int(all_pages[-1])
    except TimeoutException:
        get_number()

###获取页面内容，time.sleep(2)是为了让页面加载完成
def get_page(page):
    print('start to spide',page)
    if page>1:
        bottom = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.pager_next')))
        bottom.click()
        time.sleep(2)
    return browser.page_source

###解析网页，获取数据
def get_message(html):
    doc = pq(html)
    items = doc('.con_list_item.default_list').items()
    for item in items:
        res = {}
        res['company'] = item.attr('data-company')
        res['salary'] = item.attr('data-salary')
        res['positionname'] = item.attr('data-positionname')
        res['introduce'] = item('.industry').text()
        res['keywords'] = item('.li_b_l').text().split('\n')
        yield res

###保存数据
def save_message(results):
    for result in results:
        with open(path_save,'a',encoding='utf-8') as f:
            f.write(json.dumps(result,ensure_ascii=False)+'\n')

if __name__ == '__main__':
    MAX_page = get_number()
    for page in range(1,MAX_page+1):
        html = get_page(page)
        results = get_message(html)
        save_message(results)
        time.sleep(2)
    browser.close()
