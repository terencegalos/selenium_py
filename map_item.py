from selenium import webdriver
import time
import urllib
import requests
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains

login = "https://www.jonesrusticsigns.com/customer/account/login/"
url = "http://www.colorful-garden.com/"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    br.get(login)
    time.sleep(1)
    print "Logging in."
    
    driver.find_element_by_name("login[username]").send_keys(un)
    driver.find_element_by_name("login[password]").send_keys(pw)
    driver.find_element_by_name("send").click()
    time.sleep(5)
    print "Logged in."

def get_info(driver,link,out):
	print "Navigating to: \n" + str(link)
	driver.get(link)
	time.sleep(1)
	name = driver.find_element_by_css_selector("#add div.secondary h1").text.encode("utf-8")
	sku = driver.find_element_by_css_selector("#product_id").text.encode("utf-8")
	try:
		prodfeat = driver.find_element_by_css_selector("#add div.secondary div.productFeaturesBlock").text.encode("utf-8")
	except:
		prodfeat = "No prodfeat."
	time.sleep(1)
	desc = driver.find_element_by_css_selector("#tab-1 div").text.encode("utf-8")
	qty = driver.find_element_by_css_selector("#add div.secondary div:nth-child(7) div div div input").get_attribute("value")
	price = driver.find_element_by_id("price").text.encode("utf-8")
	try:
		image = driver.find_element_by_css_selector("#large").get_attribute("src")
	except:
		image = "No image."
	opt = [s.text for s in driver.find_elements_by_css_selector("#divOptionsBlock div.container div.opt-regular div.opt-field div.dropdown-format select option")]
	for x in range(len(opt)):
		ls = []
		ls.append(name)
		ls.append(sku)
		ls.append(desc)
		ls.append(prodfeat)
		ls.append(qty)
		ls.append(price)
		ls.append(image.replace("thumbnail.asp?file=",""))
		ls.append(opt[x])
		print ls
		out.append(ls)
		
def cat_scrape(driver,container):
	try:
		driver.find_element_by_link_text("View All").click()
		print "More items found. Loading all items..."
		time.sleep(1)
	except:
		print "All items are here."
	item = driver.find_elements_by_css_selector("div.name a")
	for it in item:
		i = it.get_attribute("href")
		print i
		container.append(i)

####################################################################################################################################################################################################################################
    


items = []
ulist = []
table = []
cats = []

with open("./csv/infile/sku.csv","rb") as infile:
	for i in infile:
		items.append(i.strip())
		
print items
with open("./csv/infile/prodlist.csv","rb") as infile2:
	for f in infile2:
		i = f.strip().split(",")
		if i[1] in items:
			print "New item found."
			print i[1]
			ulist.append(i)
		else:
			print "Item not needed."
			print i[1]
			
print "***Job Done***"
              
outfile = open("./csv/outfile/unique-product-list.csv","wb")
writer = csv.writer(outfile)
writer.writerows(ulist)