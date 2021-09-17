#!/usr/local/bin/python3

import time
import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select

with open('/tmp/pass') as file:
    password = file.read()

pp = pprint.PrettyPrinter(indent=4)

with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.goodreads.com/user/sign_in")
    driver.find_element(By.NAME, "user[email]").send_keys("mlbright@gmail.com")
    driver.find_element(By.NAME, "user[password]").send_keys(password + Keys.RETURN)

    wait.until(presence_of_element_located((By.CSS_SELECTOR,".siteHeader__primaryNavInline > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)")))

    driver.find_element(By.CSS_SELECTOR, ".siteHeader__primaryNavInline > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)").click()
    wait.until(presence_of_element_located((By.CSS_SELECTOR,".selectedShelf")))

    driver.get("https://www.goodreads.com/review/list/3123130-martin-louis-bright?shelf=read")
    wait.until(presence_of_element_located((By.CSS_SELECTOR,"#per_page")))
    select = Select(driver.find_element_by_id('per_page'))

    # select.select_by_visible_text("infinite scroll")
    select.select_by_visible_text("100")

    table = driver.find_element_by_id("books")
    rows = table.find_elements_by_tag_name("tr")

    for i in range(len(rows)):
        cells = rows[i].find_elements_by_tag_name("td")
        if len(cells) >= 8:
            fields = [c.text for c in cells[3:7]]
            print("{}".format("\t".join(fields)))
