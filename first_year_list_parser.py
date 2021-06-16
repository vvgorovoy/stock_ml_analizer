# -*- coding: utf-8 -*-
"""
Программа для парсинга первого года финансовой отчетности,
представленной на сайте и для занесения этой информации в таблицу
"""

#Загрузка необходимых библиотек
import os
import time
import pandas as pd
import numpy as np
from selenium import webdriver


def get_year(page):
    """Получение года первой финансовой отчетности, представленной на сайте"""
    browser.get(page)
    i = 2005
    while i<=2020:
        if browser.find_element_by_xpath('/html/body/div[2]/div[2]/h2').text.find(f'{i}-') > -1:
            year = i
            break
        i+=1
    return year

if not os.path.exists(r'Data/first_year_lisr.csv'):
    #Получение списка компаний из файла
    splist = pd.read_csv(r"Data/splist_for_parser.csv")

    #Создание новой таблицы
    first_year_list = splist.reindex(columns = splist.columns.tolist() + ['Year of first statement'])

    #Создание списка ссылок для парсинга
    links = []
    for gi in np.arange(len(splist.index)):
        link = f'https://www.macrotrends.net/stocks/charts/{splist.Ticker[gi]}/{splist.Company[gi]}/income-statement'
        links.append(link)

    #Открытие браузера Google Chrome
    browser = webdriver.Chrome()
    #browser.maximize_window()
    browser.set_window_size(1920, 1080)

    #Выполнение парсинга и заполнение таблицы
    for gi in np.arange(len(splist.index)):  #len(splist.index)
        link = links[gi]
        first_year_list['Year of first statement'][gi] = get_year(link)

    #Занесение готовой таблицы в новый файл и закрытие браузера
    first_year_list.to_csv(r"Data/first_year_list.csv", index = False)
    time.sleep(2)
    browser.quit()
