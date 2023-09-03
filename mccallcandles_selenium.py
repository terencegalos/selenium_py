from selenium import webdriver
import time
import urllib2
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from urllib import urlopen
import urllib
import csv

url = "http://www.mccallscandles.com/"
season = "http://www.mccallscandles.com/Shop-by-Season-Holiday/departments/49/"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):    
    driver.get("https://www.mccallscandles.com/statuslogin.asp")
    time.sleep(1)
    try:
		print "Logging in..."
		driver.find_element_by_name('regtxtemail').send_keys(un)
		driver.find_element_by_name('txtregpassword').send_keys(pw)
		driver.find_element_by_name('txtregpassword').send_keys(Keys.ENTER)
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
  
# links = ["https://www.mccallscandles.com/McCalls-Confections/departments/101/","http://www.mccallscandles.com/Candle-Bars/products/10/","http://www.mccallscandles.com/Rustic-Romance/products/148/","http://www.mccallscandles.com/Candle-Accessories/products/240/"]

#initialize and open browser
br = init_driver()
init_login(br,uname,passw)
# br.get(url)
# time.sleep(1)
# br.get(season)
# time.sleep(1)
# eachseason = br.find_elements_by_css_selector("a.allpage")
# each = [e.get_attribute("href") for e in eachseason]

table = []
items = []

# for x in range(len(links)):
	# br.get(links[x])
	# time.sleep(1)
	# print x
	# if x == 0:
		# scent = br.find_elements_by_css_selector("a.allpage")
		# scents = [s.get_attribute("href") for s in scent]
		# for sc in scents:
			# br.get(sc)
			# time.sleep(1)
			# item = br.find_elements_by_css_selector("a.producttitlelink")
			# items = [itm.get_attribute("href") for itm in item]
			# for it in items:
				# get_attribute(br,it,table)
	# elif x == 1:
		# item = br.find_elements_by_css_selector("a.producttitlelink")
		# items = [itm.get_attribute("href") for itm in item]
		# while True:
			# try:
				# br.find_element_by_css_selector("a.arrowright").click()
				# time.sleep(1)
				# item = br.find_elements_by_css_selector("a.producttitlelink")
				# itm = [itm.get_attribute("href") for itm in item]
				# for it in itm:
					# items.append(itm)
			# except:
				# break
				# print "Next page exhausted."
		# for it in items:
			# print it
			# try:
				# get_attribute(br,it,table)
			# except:
				# for i in it:
					# get_attribute(br,i,table)
	# else:
		# item = br.find_elements_by_css_selector("a.producttitlelink")
		# items = [itm.get_attribute("href") for itm in item]
		# for it in items:
			# get_attribute(br,it,table)
			
with open("./csv/infile/mccallscandles_infile.csv","rb") as row:
	for cell in row:
		print "Looking for item " + cell
		br.find_element_by_css_selector("#searchprodform > div.divheadercontent > div.divsearch > ul > li.searchbox > input").clear()
		br.find_element_by_css_selector("#searchprodform > div.divheadercontent > div.divsearch > ul > li.searchbox > input").send_keys(cell)
		#br.find_element_by_css_selector("#searchprodform > div.divheadercontent > div.divsearch > ul > li.searchbox > input").send_keys(Keys.ENTER)
		time.sleep(1)
		try:
			item = br.find_element_by_css_selector("#page-content > table.grid > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(3) > td > a").get_attribute("href")
			print item
			items.append(item)
		except:
			print "Item not found."
			
for item in items:
	get_attribute(br,item,table)
		
outfile = open("./csv/outfile/mccallscandle_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)        
br.close()