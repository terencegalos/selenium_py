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

cats =["http://www.thejunglebee.com/index.php/toe-anklets.html?limit=30","http://www.thejunglebee.com/index.php/toe-anklets.html?limit=30&p=2","http://www.thejunglebee.com/index.php/bracelets-5.html?limit=30","http://www.thejunglebee.com/index.php/anklets-29.html?limit=30"]
def init_driver():
    path = "./chrome_drive/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    

#initialize and open browser
br = init_driver()
items = []
for cat in cats:
    time.sleep(1)
    print "Navigating to: " + cat
    br.get(cat)
    links = br.find_elements_by_class_name("product-image")
    for link in links:
        lnk = link.get_attribute("href")
        items.append(lnk)
        print lnk
        
table = []
for item in items:
    ls = []
    time.sleep(1)
    print "Navigating to item: " + item

    br.get(item)
    time.sleep(1)
    name = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-name h2")))
    # name = br.find_element_by_css_selector("div.product-name h2")
    sku = br.find_element_by_css_selector("span.product-sku strong")
    desc = br.find_element_by_class_name("short-description")
    options = br.find_elements_by_css_selector("#attribute133 option")
    try:
        multi = br.find_element_by_class_name("product-pricing")
    except:
        multi = []
    price = br.find_element_by_class_name("price")
    image = br.find_element_by_class_name("lightbox-image")
    
    ls.append(name.text.encode("utf-8"))
    ls.append(sku.text.encode("utf-8"))
    ls.append(desc.text.encode("utf-8"))
    try:
        ls.append(multi.text.encode("utf-8"))
    except:
        ls.append(multi)
    ls.append(price.text.encode("utf-8"))
    ls.append([option.text.encode("utf-8") for option in options])
    ls.append(image.get_attribute("src"))
    print ls
    table.append(ls)
    
outfile = open("./csv/outfile/junglebeeresults.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
    