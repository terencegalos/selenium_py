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

login = "http://www.wtcollectionshowroom.com/cgi-wtcollectionshowroom/sb/order.cgi?func=2&storeid=*1209f4a48ae200708d5090&html_reg=html"
url = "http://www.redhorsevintage.com/"
uname = "service@waresitat.com"
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
        driver.find_element_by_name('email1').send_keys(un)
        driver.find_element_by_name('text1').send_keys(pw)
        driver.find_element_by_class_name("button166").click()
        print "Login Success."
        time.sleep(10)
    except:
        print "Login failed."
        
def get_info(driver,out):
	ls = []
	try:
		name = driver.find_element_by_css_selector("body > div.wrapper > div > div.main-container.col2-right-layout > div > div > div.col-main.col-sm-9 > div.product-view > div.product-essential > div.row > div.product-shop.col-sm-7 > div.product-name > h1").text.encode("utf-8")
	except:
		name = driver.find_element_by_css_selector("#product_addtocart_form > div.row > div.product-shop.col-sm-7 > div.product-name > h1").text.encode("utf-8")
	try:
		sku = driver.find_element_by_css_selector("body > div.wrapper > div > div.main-container.col2-right-layout > div > div > div.col-main.col-sm-9 > div.product-view > div.product-essential > div.row > div.product-shop.col-sm-7 > div.product-name > p > strong").text.encode("utf-8")
	except:
		sku = driver.find_element_by_css_selector("#product_addtocart_form > div.row > div.product-shop.col-sm-7 > div.product-name > p > strong").text.encode("utf-8")
	try:
		desc = driver.find_element_by_css_selector("body > div.wrapper > div > div.main-container.col2-right-layout > div > div > div.col-main.col-sm-9 > div.product-view > div.product-essential > div.row > div.product-shop.col-sm-7 > div.short-description > div").text.encode("utf-8")
	except:
		desc = 	driver.find_element_by_css_selector("#product_addtocart_form > div.row > div.product-shop.col-sm-7 > div.short-description > div").text.encode("utf-8")
	WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img.etalage_thumb_image")))
	image = driver.find_element_by_css_selector("img.etalage_thumb_image").get_attribute("src")
	ls.append(name)
	ls.append(sku)
	ls.append(desc)
	ls.append(image)
	print ls
	out.append(ls)
    
            

#initialize and open browser
br = init_driver()
br.get(url)
time.sleep(1)

items = []
table = []
with open("./csv/infile/redhorsevintage.csv","rb") as infile:
    for i in infile:
        print "Searching for " + i
        while True:
            try:
                br.find_element_by_css_selector("body > div.wrapper > div > div.header-container.type14 > div.header.container > div.search-area > a > i").click()
                br.find_element_by_name("q").clear()
                br.find_element_by_name("q").send_keys(i)
                time.sleep(1)
                break
            except:
                br.refresh()
                time.sleep(1)
                continue
        try:
			itm = br.find_element_by_css_selector("h2.product-name a").get_attribute("href")
			print itm
			items.append(itm)
			print "Link/s saved"
        except:
            print "Item not found."
            
print "Getting each items attributes..."

for item in set(items):
	ls = []
	print "Navigating to " + item
	br.get(item)
	time.sleep(1)
	get_info(br,table)
        # while True:
            # try:
                # break
            # except:
                # br.refresh()
                # time.sleep(1)
                # continue

            
            
outfile = open("./csv/outfile/redhorsevintage_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)    
