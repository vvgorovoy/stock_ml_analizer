# -*- coding: utf-8 -*-

"""
Программа для парсинга всех финансовых отчетностей компаний
из индекса S&P500 с 2005 по 2019 год и занесения этих данных
в таблицу
"""

#Загрузка необходимых библиотек
import os
import time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def right_scroll():
    """Прокрутка таблицы с данными вправо"""
    try:
        scroll_button_rigth_xpath = '//*[@id="jqxScrollBtnDownhorizontalScrollBarjqxgrid"]/div'
        scroll_button_right = browser.find_element_by_xpath(scroll_button_rigth_xpath)
        scroll_button_right.click()
        for i in np.arange(150):
            scroll_button_right.click()
            time.sleep(0.05)
    except Exception:
        pass

def left_scroll():
    """Прокрутка таблицы с данными влево"""
    scroll_button_left_xpath = '//*[@id="jqxScrollBtnUphorizontalScrollBarjqxgrid"]/div'
    scroll_button_left = browser.find_element_by_xpath(scroll_button_left_xpath)
    for i in np.arange(150):
        scroll_button_left.click()
        time.sleep(0.05)

def get_table(link):
    """Получение html-кода таблицы с данными"""
    browser.get(link)
    html = browser.find_element_by_tag_name('html')
    for i in np.arange(17):
        html.send_keys(Keys.DOWN)
        time.sleep(0.2)
    right_scroll()
    table = browser.find_element_by_xpath('//*[@id="jqxgrid"]')
    return table

def input_nothing(ind):
    """Заполнение списка пустым значением"""
    ind.insert(0,'')
    return ind


def fill_lists1(revenue_row, revenues, net_income_row,
                net_incomes, ebitda_row, ebitdas, j):
    """
    Занесение значений Revenue, Net Income, EBITDA в соответсвующий список
    """
    curr_year_revenue = revenue_row.find_element_by_xpath(
        f'//*[@id="row0jqxgrid"]/div[{j}]'
        )
    revenues.append(
        curr_year_revenue.text.replace("$","").replace(" ","").replace(",",".")
        )
    curr_year_net_income = net_income_row.find_element_by_xpath(
        f'//*[@id="row15jqxgrid"]/div[{j}]'
        )
    net_incomes.append(
        curr_year_net_income.text.replace("$","").replace(" ","").replace(",",".")
        )
    curr_year_ebitda = ebitda_row.find_element_by_xpath(
        f'//*[@id="row16jqxgrid"]/div[{j}]'
        )
    ebitdas.append(
        curr_year_ebitda.text.replace("$","").replace(" ","").replace(",",".")
        )

def get_income_statement_info(table, start_year):
    """
    Получение значений Revenue, Net Income, EBITDA из таблицы
    """
    revenue_row = table.find_element_by_xpath('//*[@id="row0jqxgrid"]')
    revenues = []
    net_income_row = table.find_element_by_xpath('//*[@id="row15jqxgrid"]')
    net_incomes = []
    ebitda_row = table.find_element_by_xpath('//*[@id="row16jqxgrid"]')
    ebitdas = []
    if start_year <= 2008:
        for j in np.arange(14,2,-1):
            fill_lists1(revenue_row, revenues, net_income_row,
                        net_incomes, ebitda_row, ebitdas, j
                        )
        left_scroll()
        for j in np.arange(-1998+start_year,11):
            fill_lists1(revenue_row, revenues, net_income_row,
                        net_incomes, ebitda_row, ebitdas, j
                        )
    else:
        for j in np.arange(2023-start_year,2,-1):
            fill_lists1(revenue_row, revenues, net_income_row,
                        net_incomes, ebitda_row, ebitdas, j
                        )
    num_of_nothing = int(start_year - 2005)
    for k in np.arange(num_of_nothing):
        input_nothing(revenues)
        input_nothing(net_incomes)
        input_nothing(ebitdas)
    return revenues, net_incomes, ebitdas


def fill_lists2(cash_row, cashes, debt_row, debts, t_assets_row,
                total_assets, t_liabilities_row, total_liabilities, j):
    """
    Занесение значений Cash, Debt, Total Assets,
    Total Liabilities в соответсвующий список
    """
    curr_year_cash = cash_row.find_element_by_xpath(
        f'//*[@id="row0jqxgrid"]/div[{j}]'
        )
    cashes.append(
        curr_year_cash.text.replace("$","").replace(" ","").replace(",",".")
        )
    curr_year_debt = debt_row.find_element_by_xpath(
        f'//*[@id="row13jqxgrid"]/div[{j}]'
        )
    debts.append(
        curr_year_debt.text.replace("$","").replace(" ","").replace(",",".")
        )
    curr_year_t_assets = t_assets_row.find_element_by_xpath(
        f'//*[@id="row11jqxgrid"]/div[{j}]'
        )
    total_assets.append(
        curr_year_t_assets.text.replace("$","").replace(" ","").replace(",",".")
        )
    curr_year_t_liabilities = t_liabilities_row.find_element_by_xpath(
        f'//*[@id="row16jqxgrid"]/div[{j}]'
        )
    total_liabilities.append(
        curr_year_t_liabilities.text.replace("$","").replace(" ","").replace(",",".")
        )

def get_balance_sheet_info(table, start_year):
    """
    Получение значений Cash, Debt, Total Assets,
    Total Liabilities из таблицы
    """
    cash_row = table.find_element_by_xpath('//*[@id="row0jqxgrid"]')
    cashes = []
    debt_row = table.find_element_by_xpath('//*[@id="row13jqxgrid"]')
    debts = []
    t_assets_row = table.find_element_by_xpath('//*[@id="row11jqxgrid"]')
    total_assets = []
    t_liabilities_row = table.find_element_by_xpath('//*[@id="row16jqxgrid"]')
    total_liabilities = []
    if start_year <= 2008:
        for j in np.arange(14,2,-1):
            fill_lists2(cash_row, cashes, debt_row, debts, t_assets_row,
                        total_assets, t_liabilities_row, total_liabilities, j
                        )
        left_scroll()
        for j in np.arange(-1998+start_year,11):
            fill_lists2(cash_row, cashes, debt_row, debts, t_assets_row,
                        total_assets, t_liabilities_row, total_liabilities, j
                        )
    else:
        for j in np.arange(2023-start_year,2,-1):
            fill_lists2(cash_row, cashes, debt_row, debts, t_assets_row,
                        total_assets, t_liabilities_row, total_liabilities, j
                        )
    num_of_nothing = int(start_year - 2005)
    for k in np.arange(num_of_nothing):
        input_nothing(cashes)
        input_nothing(debts)
        input_nothing(total_assets)
        input_nothing(total_liabilities)
    return cashes, debts, total_assets, total_liabilities


def input_fins_in_table(revenues, net_incomes, ebitdas, cashes, debts,
                        total_assets, total_liabilities, fin_data, num):
    """Заполнение общей таблицы с финансовыми показателями компаний"""
    k = fin_data.index[fin_data['Ticker'] == splist.Ticker[num]]
    for i in np.arange(len(debts)):
        fin_data.iloc[k, i+4] = revenues[i]
        fin_data.iloc[k, i+20] = net_incomes[i]       #2021 -> 21
        fin_data.iloc[k, i+36] = ebitdas[i]           #2021 -> 38
        fin_data.iloc[k, i+52] = cashes[i]            #2021 -> 55
        fin_data.iloc[k, i+68] = debts[i]             #2021 -> 72
        fin_data.iloc[k, i+84] = total_assets[i]      #2021 -> 89
        fin_data.iloc[k, i+100] = total_liabilities[i] #2021 -> 106
    return fin_data


if not os.path.exists(r"Data/financial_data.csv"):
    #Получение подготовленного списка компаний
    splist = pd.read_csv(r"Data/splist_for_parser.csv")

    #Создание новой таблицы
    columns = []
    finlist = ['Revenue ', 'Net Income ', 'EBITDA ', 'Cash ',
               'Debt ', 'Total Assets ', 'Total Liabilities ']
    for parameter in finlist:
        for x in np.arange(2005, 2021):#если по 2019, то "2020"; если по 2020, то - "2021"
            columns.append(parameter + str(x))
    financial_data = splist.reindex(columns = splist.columns.tolist() + columns)

    #Создание списка всех необходимых ссылок
    links1, links2 = [], []
    for g in np.arange(len(splist.index)):
        tick = splist.Ticker[g]
        comp = splist.Company[g]
        link1 = f'https://www.macrotrends.net/stocks/charts/{tick}/{comp}/income-statement'
        links1.append(link1)
        link2 = f'https://www.macrotrends.net/stocks/charts/{tick}/{comp}/balance-sheet'
        links2.append(link2)

    #Получение информации о годе первой финансовой отчетности на сайте
    first_year_list = pd.read_csv(r"Data/first_year_list.csv")
    first_years  = first_year_list['Year of first statement']

    #Открытие браузера Google Chrome
    browser = webdriver.Chrome()
    #browser.maximize_window()
    browser.set_window_size(1920, 1080)

    #financial_data = pd.read_csv("financial_data.csv")
    #Выполнение парсинга и заполнение таблицы
    for gi in np.arange(len(splist.index)):  #len(splist.index)
        try:
            link1 = links1[gi]
            link2 = links2[gi]
            first_year = first_years[gi]
            if first_year <= 2016:
                revenue_list, net_income_list, ebitda_list = get_income_statement_info(
                    get_table(link1), first_year
                    )
                cash_list, debt_list,total_assets_list, total_liabilities_list = get_balance_sheet_info(
                    get_table(link2), first_year
                    )
                input_fins_in_table(revenue_list, net_income_list, ebitda_list, cash_list,
                                    debt_list, total_assets_list, total_liabilities_list,
                                    financial_data, gi
                                    )
        except Exception:
            print(splist.Ticker[gi], 'has unusual data')

    #Занесение готовой таблицы в новый файл
    financial_data.to_csv(r"Data/financial_data.csv", index = False)

    #Закрытие браузера
    time.sleep(2)
    browser.quit()
