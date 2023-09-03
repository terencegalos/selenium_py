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
url = "https://www.acheerfulgiver.com/"
sales = "https://adamsandco.net/category.php?category=30"
farm = "https://www.acheerfulgiver.com/candles/farm-fresh.html"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):
    driver.get("https://www.acheerfulgiver.com/customer/account/login/")
    time.sleep(1)
    print "Logging in..."
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"email"))).send_keys(un)
    driver.find_element_by_id('pass').send_keys(pw)
    driver.find_element_by_css_selector("#send2 span span").click()
    print "Login Success."
    time.sleep(10)
    # except:
        # print "Login failed."
		

            

#initialize and open browser
br = init_driver()
init_login(br,uname,passw)
time.sleep(3)


items = []
table = []

#get farm fresh and show all items
# br.get(farm)
# time.sleep(1)
# br.find_element_by_css_selector("#limiter > option:nth-child(3)").click()
# time.sleep(1)

#get items and loop each
# items = [it.get_attribute("href") for it in br.find_elements_by_css_selector("h3.product-name a")]

# for i in items:
	# ls = []
	# print "Navigating to " + i
	# br.get(i)
	# time.sleep(1)
	# name = br.find_element_by_css_selector("#product_addtocart_form div.row div.col-md-8.col-sm-7 div div.product-name h1").text.encode("utf-8")
	# minqty = br.find_element_by_css_selector("#singleMainContent div.prodDetails p:nth-child(8) span")
	# price = br.find_element_by_css_selector("#singleMainContent div.prodDetails p.price_value.clearfix span")
	# case = br.find_element_by_css_selector("#singleMainContent div.prodDetails p:nth-child(7) span")
	# try:
		# print "Name successfully saved. Attempting to grab options..."
		# opt = br.find_elements_by_css_selector("select option")
		# option = []
		# for i in opt:
			# print i.text
			# option.append(i.text.encode("utf-8"))
		# image = br.find_element_by_css_selector("#zoom1").get_attribute("href")
	# except:
		# option = "No option."                    
		
	# ls.append(name)
	# ls.append(sku)
	# ls.append(option)
	# ls.append(image)
	# table.append(ls)
	# print ls    
	

with open("./csv/infile/acg.csv","rb") as infile:
    for sku in infile:
		print "\nSearching for item " + str(sku)       
		time.sleep(1)
		while True:
			try:
				br.find_element_by_name("q").clear()
				br.find_element_by_name("q").send_keys(str(sku))
				break
			except:
				br.refresh()
				time.sleep(1)
				continue
		try:
			br.find_element_by_css_selector("#limiter option:nth-child(3)").click()
			time.sleep(2)           
			item = br.find_elements_by_css_selector("h3.product-name a")
			
			for i in item:
				ls = []
				print "Navigating to " + str(i.get_attribute("href"))
				br.get(i.get_attribute("href"))                  
				try:
					time.sleep(1)
					name = br.find_element_by_css_selector("#product_addtocart_form div.row div.col-md-8.col-sm-7 div div.product-name h1").text.encode("utf-8")
					try:
						minqty = br.find_element_by_css_selector("#singleMainContent div.prodDetails p:nth-child(8) span")
					except:
						minqty = "No minqty."
					try:
						price = br.find_element_by_css_selector("#singleMainContent div.prodDetails p.price_value.clearfix span")
					except:
						price = "no price"
						print 
					try:
						case = br.find_element_by_css_selector("#singleMainContent div.prodDetails p:nth-child(7) span")
					except:
						case = "no case."
					try:
						print "Name successfully saved. Attempting to grab options..."
						opt = br.find_elements_by_css_selector("select option")
						option = []
						for i in opt:
							print i.text
							option.append(i.text.encode("utf-8"))
						image = br.find_element_by_css_selector("#zoom1").get_attribute("href")
					except:
						option = "No option."                    
                        
					ls.append(name)
					ls.append(sku)
					ls.append(option)
					ls.append(image)
					table.append(ls)
					print ls
				except Exception as e:
					print e
					time.sleep(1)
		except:
			print "No item found."

outfile = open("./csv/outfile/acg_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)                        
