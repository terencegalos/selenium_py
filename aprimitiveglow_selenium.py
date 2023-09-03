import requests
import time
import csv
from bs4 import BeautifulSoup
import urllib2
import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException

url = "http://aprimitiveglow.com/index.php?route=account/login"
links = ["http://aprimitiveglow.com/index.php?route=product/category&path=59","http://aprimitiveglow.com/index.php?route=product/category&path=60","http://aprimitiveglow.com/index.php?route=product/category&path=61","http://aprimitiveglow.com/index.php?route=product/category&path=63","http://aprimitiveglow.com/index.php?route=product/category&path=62","http://aprimitiveglow.com/index.php?route=product/category&path=64","http://aprimitiveglow.com/index.php?route=product/category&path=84","http://aprimitiveglow.com/index.php?route=product/category&path=82","http://aprimitiveglow.com/index.php?route=product/category&path=83"]
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser
    
def init_login(driver,un,pw):    
    driver.get(url)
    time.sleep(3)
    try:
        print "Logging in..."
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(un)
        driver.find_element_by_name('password').send_keys(pw)
        driver.find_element_by_xpath("//*[@id=\"content\"]/div[2]/div[2]/form/div/input[3]").click()
        time.sleep(3)
        print "Login Success."
    except:
        print "Login failed."
        
#initialize and open browser
br = init_driver()
init_login(br,uname,passw)

items = []
#scrape all items
for link in links:
    br.get(link)
    time.sleep(1)
    try:
        WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content div.product-filter div.limit select option:nth-child(5)"))).click()
        time.sleep(2)
            
        itms = br.find_elements_by_css_selector(".name a")
        for itm in itms:
            print str(itm.get_attribute("href"))
            items.append(itm.get_attribute("href"))
        
    except:
        print "No item found in this category."

print "***Scraped all categories for items."
uitems = list(set(items))
table = []

#get all items attributes
for item in uitems:

    ls = []
    br.get(item)
    time.sleep(1)
	
    name = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content h1"))).text.encode("utf-8")
    desc = br.find_element_by_css_selector("#content div.product-info div.right div.description").text.encode("utf-8")
    sku = "|".join(br.find_element_by_css_selector("#content > div.product-info > div > div.description").text.split("\n"))[0]
    cat = "|".join([o.text.encode("utf-8") for o in br.find_elements_by_css_selector("#content div.breadcrumb a")])
    # desc = ""
	
    try:
        qty = br.find_element_by_css_selector("#content div.product-info div.right div.cart div input[type=\"text\"]:nth-child(1)").get_attribute("value")
    except:
        qty = "None."
    try:
        price = br.find_element_by_id("myoc-lpu-price").text.encode("utf-8")
    except:
        price = "None."

    try:
        scents = "|".join([o.text.encode("utf-8").strip() for o in br.find_elements_by_css_selector("select option")])
    except:
        scents = "No scent available."
    
    try:
        image = br.find_element_by_css_selector("#content div.product-info div.left div a").get_attribute("href")
    except:
        image = "None"
                    
    ls.append(name)
    
    ls.append(sku)
    
    ls.append(cat)
    
    ls.append(desc)

    ls.append(qty)

    ls.append(price)

    ls.append(image)
    
    ls.append(scents)
    
    print ls
    
    table.append(ls)

    
#write to csv file
outfile = open("./csv/outfile/A_Primitive_Glow_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)    


print "***Job Done***"    