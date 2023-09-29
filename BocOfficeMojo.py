from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

# Chrome driver
driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://www.boxofficemojo.com/chart/top_lifetime_gross/?area=XWW')

# movies, year, earning (webdriver elements)
movies_name = []
years = []
earns = []
# get names of movies
movies_name_list = []
years_list = []
earns_list = []

for i in range(0, 4):
    movies_name = driver.find_elements(By.CSS_SELECTOR, value="td.mojo-field-type-title > a.a-link-normal")
    next = driver.find_element(By.CSS_SELECTOR, value="li.a-last > a")
    for j in movies_name:
        movies_name_list.append(j.text)
    years = driver.find_elements(By.CSS_SELECTOR, value="td.mojo-field-type-year > a.a-link-normal")
    for j in years:
        years_list.append(j.text)
    earns = driver.find_elements(By.CSS_SELECTOR, value="td.mojo-field-type-money")
    for j in earns:
        earns_list.append(j.text)
    next.send_keys(Keys.ENTER)

driver.quit()

# save the data
data = list(zip(movies_name_list, years_list, earns_list))

df = pd.DataFrame(data, columns=['movie_name', 'release_date', 'earning'])

df.to_csv("movie_data.csv", index=False)
driver.quit()