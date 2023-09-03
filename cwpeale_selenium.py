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
url = "http://www.cwpeale.com/"
uname = "salesrep"
passw = "adams"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser


#initialize and open browser
br = init_driver()
br.get(url)
time.sleep(1)

items = []
table = []

with open("./csv/infile/cwpeale.csv","rb") as infile:
    for i in infile:
        print "\nSearching for item " + str(i)
       
        br.find_element_by_name("q").clear()
        br.find_element_by_name("q").send_keys(str(i))
        time.sleep(1)
        try:
            item = WebDriverWait(br,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"body div div div.main-container.col3-layout div div.col-wrapper div.col-main div.category-products ul li a")))
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
        sku = WebDriverWait(br,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#product_addtocart_form div.product-shop div.short-description div")))
        image = br.find_element_by_css_selector("#image")
        
        ls.append(sku.text)
        ls.append(image.get_attribute("src"))
        table.append(ls)
        print ls
    except:
        print "Some error occurred. Skipping..."
        
outfile = open("./csv/outfile/cwpeale_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)                