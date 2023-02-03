from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

chrome_driver_path = "C:\Development\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1")
# time.sleep(120)
link_list=[]
description_list=[]
asin_list=[]
manufacturer_list=[]

def get_link_list():
    links=driver.find_elements(By.CSS_SELECTOR, 'a[class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
    for link in links:
        link_list.append(link.get_attribute('href'))
        # print(link_list)
get_link_list()
while len(link_list) <= 200:
    next_page = driver.find_element(By.CSS_SELECTOR, 'a[class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]')
    driver.get(next_page.get_attribute('href'))
    get_link_list()

# print(len(link_list))
# print(link_list)

def get_info():
    for ll in link_list:
        try:
            # print(ll)
            driver.get(ll)
            # driver.fullscreen_window()
            description = driver.find_element(By.ID, 'feature-bullets')
            desc_info=(description.text)
            description_list.append(desc_info)
            try:
                asin = driver.find_element(By.XPATH, '//*[@id="detailBullets_feature_div"]/ul/li[4]')
                asin_info=(asin.text)
                # print(asin_info)
                asin_list.append(asin_info)
                # print("asin try")
                try:
                    manufacturer_name = driver.find_element(By.XPATH, '//*[@id="detailBullets_feature_div"]/ul/li[8]')
                    manufacturer_info = (manufacturer_name.text)
                    # print(manufacturer_info)
                    manufacturer_list.append(manufacturer_info)
                except:
                    manufacturer_name = driver.find_element(By.XPATH, '// *[ @ id = "detailBullets_feature_div"] / ul / li[3]')
                    manufacturer_info = (manufacturer_name.text)
                    # print(manufacturer_info)
                    manufacturer_list.append(manufacturer_info)
            except:
                asin = driver.find_element(By.XPATH, '// *[ @ id = "productDetails_detailBullets_sections1"] / tbody / tr[1]')
                asin_info = (asin.text)
                # print(asin_info)
                asin_list.append(asin_info)
                manufacturer_name = driver.find_element(By.XPATH, '//*[@id="productDetails_techSpec_section_1"]/tbody/tr[2]')
                manufacturer_info=(manufacturer_name.text)
                # print(manufacturer_info)
                manufacturer_list.append(manufacturer_info)
            finally:
                # time.sleep(2)
                driver.back()
        except:
            driver.back()

while("" in link_list):
    link_list.remove("")


get_info()


df1 = pd.DataFrame({"Description": description_list})
df2 = pd.DataFrame({"ASIN":asin_list})
df3 = pd.DataFrame({"Manufacturer":manufacturer_list})
df4 = pd.DataFrame({"Link":link_list})
pd.concat([df1, df2, df3, df4], axis=1).to_csv('Info.csv', index=False)
