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

login = "http://www.artisticreflections.com/login.asp"
url = "http://www.wtcollectionshowroom.com/store/viewproducts.html"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):    
    driver.get(login)
    time.sleep(3)
    try:
        print "Logging in..."
        driver.find_element_by_name('email').send_keys(un)
        driver.find_element_by_name('password').send_keys(pw)
        driver.find_element_by_name("imageField2").click()
        print "Login Success."
        time.sleep(10)
    except:
        print "Login failed."
            

#initialize and open browser
br = init_driver()
init_login(br,uname,passw)

items = []
table = []

with open("./csv/infile/artisticinfile.csv","rb") as infile:
    for i in infile:
        print "\nSearching for item " + str(i)
        br.find_element_by_id("search_input").send_keys(str(i))
        time.sleep(1)
        try:
            item = br.find_element_by_css_selector("#MainForm table:nth-child(4) tbody tr td table tbody tr td table tbody tr:nth-child(2) td div a")
            items.append(item.get_attribute("href"))
            print item.get_attribute("href")
        except:
            print "No item found."
        


for i in items:
    print "Navigating to " + str(i)
    ls = []
    
    try:
        br.get(i)
        time.sleep(1)
        sku = WebDriverWait(br,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#v65-product-parent tbody tr:nth-child(2) td:nth-child(2) table tbody tr td table tbody tr:nth-child(2) td:nth-child(2) table tbody tr:nth-child(1) td:nth-child(1) div i font span.product_code")))
        cat = br.find_element_by_css_selector("#v65-product-parent tbody tr:nth-child(1) td")
        image = br.find_element_by_css_selector("#product_photo")
        
        ls.append(sku.text)
        ls.append(cat.text.encode("utf-8"))
        ls.append(image.get_attribute("src"))
        table.append(ls)
        print ls
    except:
        print "Some error occurred. Skipping..."
        
outfile = open("./csv/outfile/artistic_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)