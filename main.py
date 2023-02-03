from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import csv


chrome_driver_path = "C:\Development\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1")

link_list=[]
names_list = []
prices_list =[]
reviews_list=[]
def get_info():
    links=driver.find_elements(By.CSS_SELECTOR, 'a[class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
    for link in links:
        # print(link.get_attribute('href'))
        link_list.append(link.get_attribute('href'))
    names = driver.find_elements(By.CSS_SELECTOR, 'a[class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
    for name in names:
        # print(name.text)
        names_list.append(name.text)
    prices = driver.find_elements(By.CSS_SELECTOR, 'div[class="a-row a-size-base a-color-base"]')
    for price in prices:
        # print(price.text)
        prices_list.append(price.text)
    reviews = driver.find_elements(By.CSS_SELECTOR, ("span[class='a-size-base s-underline-text']"))
    for review in reviews:
        # print(review.text)
        reviews_list.append(review.text)

get_info()
for i in range(19):
    next_page=driver.find_element(By.CSS_SELECTOR, 'a[class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')
    driver.get(next_page.get_attribute('href'))
    get_info()

while("" in names_list):
    names_list.remove("")
while("" in prices_list):
    prices_list.remove("")
while("" in reviews_list):
    reviews_list.remove("")
while("" in link_list):
    link_list.remove("")


df1 = pd.DataFrame({"Names":names_list})
df2 = pd.DataFrame({"Price": prices_list})
df3 = pd.DataFrame({"Reviews": reviews_list})
df4 = pd.DataFrame({"Link": link_list})
pd.concat([df1, df2, df3, df4], axis=1).to_csv('myfile.csv', index=False)



driver.quit()