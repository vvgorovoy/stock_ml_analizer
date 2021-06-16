# -*- coding: utf-8 -*-

"""
Программа для парсинга капитализаций и цен на момент запуска
и создания соответсвующей таблицы с данными
"""

#Загрузка необходимых библиотек
import os
import time
import pandas as pd
import numpy as np
from selenium import webdriver


def push_sorting_mc():
    """Нажатие кнопки сортировки по капитализации"""
    sort_by_mc_button = browser.find_element_by_xpath(
        '//*[@id="js-screener-container"]/div[3]/table/thead/tr/th[7]'
        )
    sort_by_mc_button.click()
    time.sleep(1.5)
    sort_by_mc_button.click()
    time.sleep(1.5)

def push_load_more():
    """Нажатие кнопки загрузить ещё для открытия всего контента страницы"""
    load_more_button = browser.find_element_by_xpath(
        '//*[@id="js-category-content"]/div/div[2]/div[3]/span'
        )
    for k in np.arange(3):
        load_more_button.click()
        time.sleep(1.5)

if not os.path.exists(r'Data/splist_with_mc.csv'):
    #Ссылка на сайт, с которого спарсятся данные
    LINK = 'https://www.tradingview.com/symbols/SPX/components/'

    #Открытие браузера
    browser = webdriver.Chrome()
    #browser.maximize_window()
    browser.set_window_size(1920, 1080)

    browser.get(LINK)
    push_sorting_mc()
    push_load_more()

    num = int(browser.find_element_by_xpath(
        '//*[@id="js-screener-container"]/div[3]/table/thead/tr/th[1]/div/div/div[2]'
        ).text[:3])

    #Создание таблицы для новых данных
    splist = pd.DataFrame(np.arange(num*4).reshape(num,4),
                          columns = ['Company', 'Ticker', 'Market Cap', 'Price']
                          )

    #Выполнение парсинга и заполнение таблицы
    for i in np.arange(num):
        company = browser.find_element_by_xpath(
            f'//*[@id="js-screener-container"]/div[3]/table/tbody/tr[{i+1}]/td[1]/div/div[2]/span[2]'
            ).text
        ticker = browser.find_element_by_xpath(
            f'//*[@id="js-screener-container"]/div[3]/table/tbody/tr[{i+1}]/td[1]/div/div[2]/a'
            ).text
        try:
            market_cap = round(float(browser.find_element_by_xpath(
                f'//*[@id="js-screener-container"]/div[3]/table/tbody/tr[{i+1}]/td[7]'
                ).text.replace('B',''))*1000, 1)
        except Exception:
            market_cap = round(float(browser.find_element_by_xpath(
                f'//*[@id="js-screener-container"]/div[3]/table/tbody/tr[{i+1}]/td[7]'
                ).text.replace('T',''))*1000000, 1)
        price = browser.find_element_by_xpath(
            f'//*[@id="js-screener-container"]/div[3]/table/tbody/tr[{i+1}]/td[2]'
            ).text
        splist.loc[i] = [company, ticker, market_cap, price]
    browser.quit()

    #Удаление строк с дублирующимися компаниями
    j=0
    while j < num-5:
        if splist.Ticker[j] in ['GOOG', 'DISCK', 'FOX', 'UA', 'NWS']:
            splist = splist.drop(index = j).reset_index(drop = True)
        else:
            j+=1

    #Занесение готовой таблицы в новый файл
    splist.to_csv(r"Data/splist_with_mc.csv", index = False)
