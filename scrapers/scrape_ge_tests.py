#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import scrape_common as sc
import scrape_ge_common as sgc


chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)

url = 'https://infocovid.smc.unige.ch/'
driver.get(url)
elem = driver.find_element_by_link_text('Graphiques')
elem.click()
elem = driver.find_element_by_partial_link_text('Tests')
elem.click()

# wait for the element
wait = WebDriverWait(driver, 10)
elem = wait.until(EC.element_to_be_clickable((By.ID, 'save_plot_nombre_tests_data')))
xls_url = elem.get_attribute('href')
assert xls_url, "Couldn't find XLS url"

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0, enable_float=True)
for row in rows:
    td = sc.TestData(canton='GE', url=url)
    res = re.search(r'(\d{2})-(\d{2})', row['week_res'])
    assert res, f"failed to extract year and week from {row['week_res']}"
    td.week = int(res[2])
    td.year = f'20{res[1]}'
    td.positive_tests = int(row['positifs'])
    td.negative_tests = int(row['négatifs'])
    td.total_tests = int(row['total'])
    # 2020-02/03 values are empty
    td.positivity_rate = 0
    if row['ratio']:
        td.positivity_rate = float(row['ratio'])
    print(td)
