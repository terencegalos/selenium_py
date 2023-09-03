from selenium import webdriver
import time
import urllib2
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from urllib import urlopen
import urllib
import csv

login = "http://www.artisticreflections.com/login.asp"
url = "http://www.annclarkcookiecutters.com/"
sitemap = "http://www.annclarkcookiecutters.com/site_map"
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
br.get(sitemap)
time.sleep(1)

item = [i.get_attribute("href") for i in br.find_elements_by_css_selector("a.subcat")]

items = []
table = []

with open("./csv/infile/annclark.csv","rb") as infile:
    for i in infile:
        print "\nSearching for item " + str(i)
        while True:
			try:
				br.find_element_by_name("keyword").clear()
				br.find_element_by_name("keyword").send_keys(i)
				br.find_element_by_name("keyword").send_keys(Keys.ENTER)
				break
			except:
				br.refresh()
				time.sleep(1)
				continue
        time.sleep(1)
        try:
			item = br.find_elements_by_css_selector("div.content a")
			for itm in item:
				i = itm.get_attribute("href")
				print i
				items.append(i)
        except:
            print "Item not found."
        
ulist = list(set(items))
for i in ulist:
	print "Navigating to " + str(i)
	ls = []
    
	br.get(i)
	time.sleep(1)
	name = br.find_element_by_css_selector("#content > form > section > div.info.iefix > div.content > h1").text.encode("utf-8")
	sku = WebDriverWait(br,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#content > form > section > div.info.iefix > div.content > div.sku"))).text.encode("utf-8")
	cat = br.find_element_by_id("breadcrumb").text.encode("utf-8")
	try:
		dim = br.find_element_by_css_selector("#content div:nth-child(2) form section div.info.iefix div.order div div.product_description_text li").text.encode("utf-8")
	except:
		dim = "No dim."
	desc1 = br.find_element_by_css_selector("#product_desc").text.encode("utf-8")
	try:
		desc2 = br.find_element_by_css_selector("#content form section div.info.iefix div.order div div.product_description_text li:nth-child(6)").text.encode("utf-8")
	except:
		desc2 = "None"
	image = br.find_element_by_css_selector("#content > form > section > div.image.iefix > a > img").get_attribute("src")
	
	ls.append(name)
	ls.append(sku)
	ls.append(cat)
	ls.append(dim)
	ls.append(desc1)
	ls.append(desc2)
	ls.append(image)
	table.append(ls)
	print ls        
outfile = open("./csv/outfile/annclark_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)        