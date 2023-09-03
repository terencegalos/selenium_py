from selenium import webdriver
import time
import urllib2
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from urllib import urlopen
import urllib
import csv

url = "http://wholesale.mccallscandles.com/"
login = "http://wholesale.mccallscandles.com/?page_id=9"
uname = "waresitat"
passw = "portal16!mcc"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser
    
def init_login(driver,pw):
	driver.get(login)
	time.sleep(1)
	try:
		print "Logging in..."
		driver.find_element_by_name('post_password').send_keys(pw)
		driver.find_element_by_name("Submit").click()
		time.sleep(1)
		print "Login Success."
	except:
		print "Login failed."
		br.close()
        
def get_items(driver,container):
    print "Getting all items in this page..."
    item = driver.find_elements_by_css_selector("a.popup.cboxElement")
    catlink = []
        
    for it in item:
        print [it.get_attribute("href")]
        catlink.append(it.get_attribute("href"))
        try:
            select = Select(driver.find_element_by_name("subCat"))
            cattext = select.first_selected_option
            print cattext.text
            catlink.append(cattext.text.encode("utf-8").strip())
        except:
            print "No category to insert in a list."
		
        print catlink
        container.append(catlink)
        catlink = []
        
def get_attribute(driver,link,container):
	driver.get(link)
	time.sleep(1)
	name = driver.find_element_by_css_selector("#page-content table:nth-child(3) tbody tr td h1").text.encode("utf-8")
	cat = driver.find_element_by_css_selector("td.breadcrumbrow").text.encode("utf-8")
	try:
		desc = driver.find_element_by_css_selector("td.plaintext.proddesc").text.encode("utf-8")
	except:
		desc = "No description."
	try:
		minqty = driver.find_element_by_name("txtquanto").get_attribute("value")
	except:
		minqty = "No minimum."
	price = driver.find_element_by_css_selector("td.ProductPrice").text.encode("utf-8")
	sku = driver.find_element_by_css_selector("td.plaintextbold").text.encode("utf-8")
	image = driver.find_element_by_css_selector("img.ProdInfoImage").get_attribute("src")
	
	ls = []
	ls.append(name)
	ls.append(sku)
	ls.append(cat)
	ls.append(desc)
	ls.append(minqty)
	ls.append(price)
	ls.append(image)
	container.append(ls)
	print ls
    

def paginator(driver,container):
	while True:
		try:
			driver.find_element_by_css_selector("#pageNav tbody tr td:nth-child(3) a").click()
			print "Next page click3d...."
			time.sleep(1)
			get_items(driver,container)
		except:
			print "Next page exhausted."
			break
            

#initialize and open browser
br = init_driver()
br.get(url)
init_login(br,passw)
time.sleep(1)
table = []
items = []

# candles = br.find_elements_by_css_selector("form h2")
# price = br.find_elements_by_css_selector("form ul")

# for x in range(len(candles)):
	# ls = []
	# name = candles[x].text.encode("utf-8")
	# pricebreak = price[x].text.encode("utf-8")
	
	# ls.append(name)
	# ls.append(pricebreak)
	# table.append(ls)
	# print ls
	
with open("./csv/infile/mccalls_infile.csv","rb") as row:
	for cell in row:
		print "Looking for item " + cell
		br.find_element_by_css_selector("#searchprodform > div.divheadercontent > div.divsearch > ul > li.searchbox > input").clear()
		br.find_element_by_css_selector("#searchprodform > div.divheadercontent > div.divsearch > ul > li.searchbox > input").send_keys(cell)
		br.find_element_by_css_selector("#searchprodform > div.divheadercontent > div.divsearch > ul > li.searchbox > input").send_keys(Keys.ENTER)
		time.sleep(1)
		try:
			item = br.find_element_by_css_selector("#page-content > table.grid > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(3) > td > a").get_attribute("href")
			print item
			items.append(item)
		except:
			print "Item not found."
			
for item in items:
	get_attribute(br,item,table)

		
outfile = open("./csv/outfile/mccandles_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)        
br.close()