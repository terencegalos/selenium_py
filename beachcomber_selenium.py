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

uname = "waresitat"
pw = "wolfville"
login = "http://www.beachcombertrading.com/Content/22.htm"
table = []
items = []
urls = []
cats = ["http://www.beachcombertrading.com/Cat-24-1-126-0/nautical-flags-6-x-9-.htm?SortOrder=4","http://www.beachcombertrading.com/Cat-24-1-124/coastal-sign-collection.htm","http://www.beachcombertrading.com/Cat-24-1-127-0/nautical-flags-7-x-12-.htm?SortOrder=4","http://www.beachcombertrading.com/Cat-24-1-141-0/coastal-sealife-collection.htm?SortOrder=4"]
def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]
    
def init_login(driver,un,passw):    
    driver.get(login)
    time.sleep(1)
    try:
        print "Logging in..."
        WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "UserName"))).send_keys(un)
        WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "Password"))).send_keys(passw)
        WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "LogonSave"))).click()
        time.sleep(3)
        print "Login Success."
    except:
        print "Login failed."
        
br = init_driver()
init_login(br,uname,pw)        

print "Getting items for the rest of the categories. ***"       
for cat in cats:
    print "Adding link or urls list.."
    urls.append(cat)
    print cat
print "Done.**"

print "Getting each item's url..***"

for url in urls:
    print "Getting items in: " + url
    br.get(url)
    time.sleep(1)
    itms = br.find_elements_by_css_selector("td.DefaultText.CatPicCell div a")
    for i in itms:
        print [i.get_attribute("href")]
        items.append(i.get_attribute("href"))
        

 
print "Printing all items scraped."
print "Getting each item's info***"
for item in items:
    ls = []    
    print "Getting info for item: " + item
    br.get(item)
    time.sleep(1)
    name = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "td.PrimaryBoldText.COMProdHeader")))
    sku = br.find_element_by_id("ProductItemCode")
    desc = br.find_element_by_css_selector("span.COMProdDesc")
    try:
        dim = br.find_element_by_class_name("COMProdDimensions")
    except:
        print "No dimension found.**"
        dim = "None"
    try:
        qty = br.find_element_by_css_selector("input#ProductQuantity.FormElementInput")
    except:
        qty = "None"
    price = br.find_element_by_css_selector("span.COMProdBasePrice")
    br.find_element_by_css_selector("div.ViewLarger a").click()
    time.sleep(2)
    try:
        img = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.tcontent img")))
    except:
        img = "None"
    try:
        ls.append(name.text.encode("utf-8"))
    except UnexpectedAlertPresentException:
        alert = br.switch_to_alert()
        alert.accept()
        time.sleep(1)
        ls.append(name.text.encode("utf-8"))
    ls.append(sku.text.encode("utf-8"))
    ls.append(desc.text.encode("utf-8"))
    try:
        ls.append(dim.text.encode("utf-8"))
    except:
        ls.append(dim)
    try:
        ls.append(qty.get_attribute("value"))
    except:
        ls.append(qty)
    ls.append(price.text.encode("utf-8"))
    try:
        ls.append(img.get_attribute("src"))
    except:
        ls.append(img)
    table.append(ls)
    print ls

    
    
outfile = open("./csv/outfile/beachcomberitems.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)    