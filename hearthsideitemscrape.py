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

table = []        
with open("./csv/infile/hearthsideitemsearchresults3.csv","rb") as infile:
    for i in infile:
        ls = []
        while True:
            try:    
                print "Navigating to " + i
                br.get(i)
                sku = WebDriverWait(br, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "sku")))        
                time.sleep(1)
                image = WebDriverWait(br, 10).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "View larger image")))
                category = WebDriverWait(br, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.breadcrumbs")))
                ls.append(sku.text.encode("utf-8"))
                ls.append(category.text.encode("utf-8"))
                ls.append(image.get_attribute("href"))
                table.append(ls)
                print ls           
            except:
                continue
                br.refresh()
                time.sleep(5)
            else:
                break

        
outfile = open("./csv/outfile/hearthsideitemscraperesults3.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)        