#MAKE SURE MAXIMIZE WINDOW

from selenium import webdriver
import time
import urllib2
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from urllib import urlopen
import urllib
import csv

url = "https://blossombucket.com/login"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):    
    driver.get(url)
    time.sleep(3)
    try:
        print "Logging in..."
        driver.find_element_by_class_name('email').send_keys(un)
        driver.find_element_by_class_name('password').send_keys(pw)
        driver.find_element_by_xpath("/html/body/div[9]/div[4]/div[5]/div/div/div[1]/div/div[2]/div[1]/div[2]/div[2]/form/div[5]/input").click()
        print "Login Success."
    except:
        print "Login failed."
        br.close()
        
#initialize and open browser
br = init_driver()
init_login(br,uname,passw)

table = []

#search items
items = []
with open("./csv/infile/blossombucket_infile.csv","rb") as infile:
    for i in infile:
        time.sleep(1)
        print "Searching item: " + i
        while True:
            try:
                br.find_element_by_id("small-searchterms").clear()
                br.find_element_by_id("small-searchterms").send_keys(i)
                break
            except:
                br.refresh()
                time.sleep(1)
                continue
        try:
            time.sleep(1)
            item = br.find_element_by_css_selector(".product-title a")
            itm = item.get_attribute("href")
            items.append(itm)
            print itm
        except:
            print "Item not found."
            
            

for i in items:
    ls = []
    time.sleep(1)
    print "Navigating to: " + i
    br.get(i)
    time.sleep(1)
    name = br.find_element_by_tag_name("h1").text.encode("utf-8")
    sku = br.find_element_by_css_selector(".sku span.value")
    category = br.find_element_by_class_name("breadcrumb")
    image = br.find_element_by_id("cloudZoomImage")
    ls.append(name)
    ls.append(sku.text.encode("utf-8"))
    ls.append(category.text.encode("utf-8"))
    ls.append(image.get_attribute("src"))
    table.append(ls)
    print ls

        
outfile = open("./csv/outfile/blossombucket_ouput.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

