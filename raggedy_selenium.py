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
sales = "https://www.adamsandco.net/clearance.html"
uname = "salesrep"
passw = "adams"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):
	driver.get(login)
	time.sleep(10)
	print "Logging in..."
	driver.find_element_by_css_selector("#topbar div div div.quicknav.col-tablet-7.collapse.topbar-collapse ul li:nth-child(3) a").click()
	time.sleep(1)
	WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,"username"))).send_keys(un)
	driver.find_element_by_name('password').send_keys(pw)
	driver.find_element_by_css_selector("input.formbutton").click()
	print "Login Success."
	time.sleep(10)

def item_prop(driver,item,container):
	driver.get(item)
	time.sleep(1)
	name = driver.find_element_by_css_selector("#listing-page-cart-inner h1 span").text.encode("utf-8")
	image = driver.find_element_by_css_selector("li#image-0 img").get_attribute("src")
	
	ls = []
	ls.append(name)
	ls.append(image)
	container.append(ls)
	print ls

#initialize and open browser
br = init_driver()
br.get("https://www.etsy.com/shop/RaggedyJunction/items")
time.sleep(5)

items = []
table = []

items = [s.get_attribute("href") for s in br.find_elements_by_css_selector("a.buyer-card.card")]
print items

for item in items:
	while True:
		try:
			print "Navigating to: " + str(item)
			item_prop(br,item,table)
			time.sleep(1)
			break
		except:
			br.refresh()
			continue
	

outfile = open("./csv/outfile/raggedy_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)