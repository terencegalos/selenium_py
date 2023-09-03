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

login = "https://adamsandco.net/home.php"
url = "https://www.shoppinecreek.com/customer-login.html"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
	

def init_login(driver,un,pw):
    time.sleep(3)
    print "Logging in..."
    time.sleep(1)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,"Customer_LoginEmail"))).send_keys(un)
    driver.find_element_by_name('Customer_Password').send_keys(pw)
    driver.find_element_by_name('Customer_Password').send_keys(Keys.ENTER)
    print "Login Success."
    time.sleep(3)
    # except:
        # print "Login failed."
def get_info(driver,out):
	ls = []
	name = driver.find_element_by_css_selector("#JS_PROD > div.content-container > div > div > div > div.row > div.col-sm-7 > h1").text.encode("utf-8")
	sku = driver.find_element_by_css_selector("#JS_PROD > div.content-container > div > div > div > div.row > div.col-sm-7 > div.prod-code > em").text.encode("utf-8")
	try:
		cat = driver.find_element_by_css_selector("#main-content div:nth-child(5)").text.encode("utf-8")
	except:
		cat = "No cat"
	minqty = driver.find_element_by_css_selector("#JS_PROD > div.content-container > div > div > div > div.row > div.col-sm-7 > form > div.well.well-prod > div > div.col-sm-3.col-xs-4 > select > option:nth-child(1)").get_attribute("value")
	try:
		price = driver.find_element_by_css_selector("#price-value").text.encode("utf-8")
	except:
		price = "No price."
	try:
		image = driver.find_element_by_css_selector("#main_image").get_attribute("src")
		print image
	except:
		image = "No image."
	
	ls.append(name)
	ls.append(sku)
	ls.append(cat)
	ls.append(minqty)
	
	ls.append(price)
	ls.append(image)
	print ls
	out.append(ls)

#initialize and open browser
br = init_driver()
#br.get(url)
#init_login(br,uname,passw)
br.get("https://www.shoppinecreek.com")
time.sleep(1)

table = []

with open("./csv/infile/pinecreek.csv","rb") as infile:
	for i in infile:
		print "\nSearching for item " + str(i)
		while True:
			try:
				br.find_element_by_name("Search").clear()
				br.find_element_by_name("Search").send_keys(i)
				time.sleep(3)
				break
			except:
				br.refresh()
				time.sleep(1)
				continue
		try:
			br.find_element_by_css_selector("#JS_SRCH > div.content-container > div > div > div > div.row.row-masonry > div.ctgy-item > a").click()
			time.sleep(1)
			try:
				get_info(br,table)
			except e:
				print e
		except:
			try:
				br.find_element_by_css_selector("#JS_PROD > div.content-container > div > div > div > div.row > div.col-sm-7 > div.well.well-prod > a").click()
				time.sleep(1)
				init_login(br,uname,passw)
			except:
				print "Item not found."
				
outfile = open("./csv/outfile/pinecreek_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()