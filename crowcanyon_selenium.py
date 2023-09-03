from selenium import webdriver
import time
import urllib
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv


uname = "service@waresitat.com"
passw = "wolfville"
login = "https://www.hcbyraghu.com/index.php?main_page=login"
url = "http://www.hcbyraghu.com/"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    driver.get(url)
    driver.find_element_by_css_selector("#logoWrapper div:nth-child(2) table tbody tr:nth-child(2) td:nth-child(1) a:nth-child(3)").click()
    time.sleep(1)
    print "Logging in."
    # try:
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID, "login-email-address"))).send_keys(un)
    driver.find_element_by_id("login-password").send_keys(pw)
    driver.find_element_by_css_selector("#loginForm div.buttonRow.forward input[type=\"image\"]").click()
    time.sleep(5)
    print "Logged in."
    # except:
        # print "Log in failed."
        # driver.close()    
 

br = init_driver()
time.sleep(3)

links = ["http://www.crowcanyonhome.com/collections/all?page=1","http://www.crowcanyonhome.com/collections/all?page=2","http://www.crowcanyonhome.com/collections/all?page=3","http://www.crowcanyonhome.com/collections/all?page=4"]

items = []
table = []

for link in links:
    br.get(link)
    time.sleep(1)
    item = br.find_elements_by_css_selector("#main div.pagecontent ul.products-list li a")
    for i in item:
        itm = i.get_attribute("href")
        print itm
        items.append(itm)
        
for i in items:
    ls = []
    br.get(i)
    time.sleep(1)
    name = br.find_element_by_css_selector("#main div.product-detail div.descr h1").text.encode("utf-8")
    sku = br.find_element_by_css_selector("#main div.product-detail div.descr strong").text.encode("utf-8")
    cat = "|".join([i.text.encode("utf-8") for i in br.find_elements_by_css_selector("#main > ul > li")])
    
	
    try:
        desc = br.find_element_by_css_selector("#main div.product-detail div.descr div.page div div").text.encode("utf-8")
    except:
        desc = br.find_element_by_css_selector("#main div.product-detail div.descr").text.encode("utf-8")
    img = WebDriverWait(br,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#main div.product-detail div.product-gallery.gallery-js-ready.autorotation-disabled div.slideset div img")))
    image = []
    for im in img:
        i = im.get_attribute("src")
        image.append(i)
    
    ls.append(name)
    ls.append(sku),ls.append(cat)
    ls.append(desc)
    ls.append(image)
    
    print ls
    table.append(ls)

print "***JOB DONE***"

outfile = open("./csv/outfile/crowcanyon_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)        