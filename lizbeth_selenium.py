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

url = "http://www.lizbethjanedesigns.com/"
uname = "waresitat"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):    
    driver.get("http://lizbeth.cameoez.com/Scripts/PublicSite/?template=Login")
    time.sleep(2)
    try:
        print "Logging in..."
        driver.find_element_by_name('username').send_keys(un)
        driver.find_element_by_name('password').send_keys(pw)
        driver.find_element_by_css_selector("#loginWrapper tbody tr:nth-child(2) td:nth-child(1) form table tbody tr:nth-child(3) td:nth-child(2) input[type=\"submit\"]").click()
        print "Login Success."
    except:
        print "Login failed."
        br.close()
        
def get_items(driver,container):
	# select = Select(driver.find_element_by_name("subCat"))
	# cattext = select.first_selected_option
	# print cattext.text
	print "Getting all items in this page..."
	item = driver.find_elements_by_css_selector("a.popup.cboxElement")
	catlink = []
	for it in item:
		print [it.get_attribute("href")]
		catlink.append(it.get_attribute("href"))
		# catlink.append(cattext.text.encode("utf-8"))
		print catlink
		container.append(catlink)
		catlink = []

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
time.sleep(1)
init_login(br,uname,passw)
time.sleep(2)

table = []
items = []

cat = br.find_elements_by_css_selector("body div div.wrap div table tbody tr td a.catpic")
cats = [c.get_attribute("href") for c in cat]
for x in range(1,len(cats)):
	br.get(cats[x])
	time.sleep(1)
	try:
		sub = br.find_element_by_name("subCat")
		subcat = sub.find_elements_by_css_selector("option")
		#click first subcategory
		br.find_element_by_css_selector("td:nth-child(1) a.category").click()
		time.sleep(1)
		get_items(br,items)
		paginator(br,items)
		for sc in range(1,len(subcat)-1):
			try:
				sub = br.find_element_by_name("subCat")
				subcat = sub.find_elements_by_css_selector("option")
				subcat[sc].click()
			except:
				print "No subcategory found for this category."
			get_items(br,items)
			paginator(br,items)
	except:
		print "No subcategory found in this category. Getting items here instead."
		get_items(br,items)
		paginator(br,items)
		
		
ulist = list(set(items))	

outfile1 = open("./csv/outfile/lizbeth_items.csv","wb")
writer1 = csv.writer(outfile1)
writer1.writerows(ulist)

for prod in ulist:
	print prod


outfile = open("./csv/outfile/lizbethjanedesigns_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)        
