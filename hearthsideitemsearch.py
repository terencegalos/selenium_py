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

url = "https://www.thehearthsidecollection.com/store/index.php?dispatch=auth.login_form&return_url=index.php%3Fdispatch%3Dproducts.view%26product_id%3D33885"
uname = "service@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_drive/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):    
    driver.get(url)
    time.sleep(3)
    try:
        print "Logging in..."
        # driver.find_element_by_id('login_').send_keys(un)
        WebDriverWait(br, 10).until(EC.visibility_of_element_located((By.ID, "login_"))).send_keys(un)
        driver.find_element_by_id('psw_').send_keys(pw)
        driver.find_element_by_class_name("button-submit-action").click()
        print "Login Success."
        time.sleep(5)
    except:
        print "Login failed."
br = init_driver()
init_login(br,uname,passw)

items = []        
with open("./csv/infile/hearthsideitemsearch.csv","rb") as infile:
    for i in infile:
        try:
            br.find_element_by_id("quick_search").clear()
            WebDriverWait(br, 10).until(EC.visibility_of_element_located((By.ID, "quick_search"))).send_keys(i)            
            time.sleep(3)
            # item = br.find_elements_by_class_name("product-title")
            item = WebDriverWait(br, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "product-title")))
            itm = item.get_attribute("href")
            items.append(itm)
            print itm
        except:
            print "No such item found."
        
outfile = open("./csv/outfile/hearthsideitemsearchresults3.csv","wb")
writer = csv.writer(outfile)
writer.writerow(items)        