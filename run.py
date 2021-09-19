#!/usr/local/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select

user = "mlbright@gmail.com"

with open("/tmp/goodreads-pass") as file:
    password = file.read()

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

# Sign in to goodreads.com
driver.get("https://www.goodreads.com/user/sign_in")
driver.find_element(By.NAME, "user[email]").send_keys(user)
driver.find_element(By.NAME, "user[password]").send_keys(password + Keys.RETURN)

# Wait for the 'My Books' link to show up, and click it
wait.until(
    presence_of_element_located(
        (
            By.CSS_SELECTOR,
            ".siteHeader__primaryNavInline > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)",
        )
    )
)
driver.find_element(
    By.CSS_SELECTOR,
    ".siteHeader__primaryNavInline > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)",
).click()

# Wait for the 'Read' link to appear
wait.until(presence_of_element_located((By.CSS_SELECTOR, ".selectedShelf")))

# Click the 'Read' link
driver.get(
    "https://www.goodreads.com/review/list/3123130-martin-louis-bright?shelf=read"
)

# Wait until the pagination dropdown shows up
wait.until(presence_of_element_located((By.CSS_SELECTOR, "#per_page")))

# Select 100 books per page
select = Select(driver.find_element_by_id("per_page"))
select.select_by_visible_text("100")

# Find all the rows in the books table
table = driver.find_element_by_id("booksBody")
rows = table.find_elements_by_tag_name("tr")

# For each row, take the book title, author, and date added
for i in range(len(rows)):
    cells = rows[i].find_elements_by_tag_name("td")
    fields = [c.text for c in cells[3:5]]
    fields.append(cells[23].text)
    print("\t".join(fields))

driver.quit()
