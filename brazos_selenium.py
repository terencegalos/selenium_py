from selenium import webdriver
import time
import urllib2
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from urllib import urlopen
import urllib
import csv

login = "https://adamsandco.net/home.php"
url = "http://www.brazos-walking-sticks.com/index.php"
uname = "salesrep"
passw = "adams"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser

def init_login(driver,un,pw):    
    driver.get(login)
    time.sleep(6)
    print "Logging in..."
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#header div ul li:nth-child(1) a"))).click()
    time.sleep(1)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,"username"))).send_keys(un)
    driver.find_element_by_name('password').send_keys(pw)
    driver.find_element_by_css_selector("input.formbutton").click()
    print "Login Success."
    time.sleep(10)
    # except:
        # print "Login failed."
            

#initialize and open browser
br = init_driver()
br.get(url)
time.sleep(1)

items = []
table = []

with open("./csv/infile/brazos-walking-sticks.csv","rb") as infile:
    for i in infile:
        print "\nSearching for item " + str(i)       
        time.sleep(1)
        WebDriverWait(br,10).until(EC.presence_of_element_located((By.ID,"search_query"))).clear()
        br.find_element_by_id("search_query").send_keys(str(i))
        time.sleep(2)

        try:
            item = br.find_elements_by_css_selector("div.ProductName strong a")
            for i in item:
                items.append(i.get_attribute("href"))
                print i.get_attribute("href")
        except:
            print "No item found."
uls = list(set(items))        
for i in uls:
    print "Navigating to " + str(i)
    ls = []
    try:
        br.get(i)
        time.sleep(1)
        sku = WebDriverWait(br,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.VariationProductSKU")))
        br.find_element_by_id("ProductDescription_Tab").click()
        time.sleep(1)
        desc = br.find_element_by_css_selector("#ProductDescription div")
        image = br.find_element_by_css_selector("div.ProductThumbImage a")
        
        ls.append(sku.text.encode("utf-8"))
        ls.append(desc.text.encode("utf-8"))
        ls.append(image.get_attribute("href"))
        table.append(ls)
        print ls
    except:
        print "skipping to next item..."
        
outfile = open("./csv/outfile/brazos-walking-sticks.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)                