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
    # except:
        # print "Login failed."
            

#initialize and open browser
br = init_driver()
time.sleep(1)

items = []
table = []

# with open("./csv/infile/adamsco.csv","rb") as infile:
    # for i in infile:
        # print "\nSearching for item " + str(i)
        # br.find_element_by_css_selector("#header div ul li:nth-child(2) a").click()
       
        # time.sleep(1)
        # br.find_element_by_id("stext").clear()
        # br.find_element_by_id("stext").send_keys(str(i))

        # try:
            # item = br.find_element_by_css_selector("#main_col div.theProds.clearfix.theProds3.alignright.eqcol div div div h5 a")
            # items.append(item.get_attribute("href"))
            # print item.get_attribute("href")
        # except:
            # print "No item found."
        
        
br.get(sales)
time.sleep(1)
while True:
	try:
		item = br.find_elements_by_css_selector("div.title a h3")
		time.sleep(1)
		for i in item:
			items.append(i.text.encode("utf-8"))
			print i.text
		br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		br.find_element_by_css_selector("ul.pagination li:nth-child(7) a ").click()
		time.sleep(1)
	except:
		print "Next page exhausted."
		break
# for i in items:
    # print "Navigating to " + str(i)
    # ls = []
    
    # try:
        # br.get(i)
        # time.sleep(1)
        
        # sku = WebDriverWait(br,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#singleMainContent div.prodDetails p:nth-child(5)")))
        # name = br.find_element_by_css_selector("#singleMainContent div.prodDetails h1")
        # minqty = br.find_element_by_css_selector("#singleMainContent div.prodDetails p:nth-child(8) span")
        # price = br.find_element_by_css_selector("#singleMainContent div.prodDetails p.price_value.clearfix span")
        # case = br.find_element_by_css_selector("#singleMainContent div.prodDetails p:nth-child(7) span")
        # image = br.find_element_by_css_selector("#zoom1 img")
        
        # ls.append(name.text.encode("utf-8"))
        # ls.append(sku.text.encode("utf-8"))
        # ls.append(minqty.text.encode("utf-8"))
        # ls.append(price.text.encode("utf-8"))
        # ls.append(case.text.encode("utf-8"))
        # ls.append(image.get_attribute("src"))
        # table.append(ls)
        # print ls
    # except:
        # print "Some error occurred. Skipping..."
        
outfile = open("./csv/outfile/adamsco_sale_results.csv","wb")
writer = csv.writer(outfile)
writer.writerow(items)