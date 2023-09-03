from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv

uname = "rstuart"
pw = "Wolfville4"
URL = "https://www.carsonhomeaccents.com/security_logon.asp?autopage=%2Fdefault%2Easp"
items = []

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser
    
def init_login(driver,un,pw):    
    driver.get(URL)
    try:
        print "Logging in..."
        driver.find_element_by_id('logonUsername').send_keys(un)
        driver.find_element_by_id('logonPassword').send_keys(pw)
        driver.find_element_by_name('B1').click()

        print ("Login Success.")
    except:
        print "Login failed."
		
def get_info():
	skus = br.find_elements_by_css_selector("div.item_row.sku.sku_original")
	for sku in skus:
		ls = []
		ls.append(sku.text.split()[1])
		ls.append(cat)
		print ls
		table.append(ls)
		
def pagination_attempt():
	while True:
		try:
			br.find_element_by_link_text("next").click()
			time.sleep(1)
			print "...next page"
			get_info()
		except:
			print "Pagination exhausted."
			break
	
def rem_filter():
	print "Removing filter..."
	while True:
		try:
			br.find_element_by_link_text("Clear All").click()
			break
		except:
			br.refresh()
			time.sleep(1)
			continue	
	
#initialize and open browser
br = init_driver()
init_login(br,uname,pw)

items = []
table = []

cats = [cat.get_attribute("href") for cat in br.find_elements_by_css_selector("#megamenu1 > div > h3 > a")]
for cat in cats:
	print "Category visit: " + cat
	br.get(cat)
	time.sleep(3)
	#get total number of cats to be expanded
	expander = br.find_elements_by_css_selector("div.nys_subtitle.ui-dialog-titlebar.ui-widget-header.ui-corner-all")
	#click each cat
	for x in range(1,len(expander)):
		while True:
			try:
				cat = br.find_elements_by_css_selector("div.nys_subtitle.ui-dialog-titlebar.ui-widget-header.ui-corner-all")[x].text.encode("utf-8")
				break
			except:
				br.back()
				time.sleep(1)
				rem_filter()
				time.sleep(1)
		
		#show cats subcats
		print "Clicking current cat."
		br.find_elements_by_css_selector("div.nys_subtitle.ui-dialog-titlebar.ui-widget-header.ui-corner-all")[x].click()
		time.sleep(2)
		
		#get subcats
		subcats = br.find_elements_by_css_selector("div.nys_section")[x]
		subcats = subcats.find_elements_by_css_selector("label > input[type=\"checkbox\"]")
		
		#check each subcats
		for s in range(len(subcats)):
			subcats = br.find_elements_by_css_selector("div.nys_section")[x]
			if subcats.find_elements_by_css_selector("label > input[type=\"checkbox\"]")[s].get_attribute("disabled") == "disabled":
				continue
			checkbox = subcats.find_elements_by_css_selector("label > input[type=\"checkbox\"]")[s]
			
			#selecting subcat
			while True:
				try:
					checkbox.click()
					break
				except:
					br.find_elements_by_css_selector("div.nys_subtitle.ui-dialog-titlebar.ui-widget-header.ui-corner-all")[x].click()
					time.sleep(1)
					checkbox.click()
					break
				else:
					br.refresh()
					time.sleep(1)
					continue
			time.sleep(1)
			
		#get product info
		get_info()
			
		#pagination if available with get_info()
		pagination_attempt()
		
		#remove filter then proceed to next cat
		rem_filter()
		
	
outfile = open('./csv/outfile/carson_cat_results.csv','wb')
writer = csv.writer(outfile)
writer.writerows(table)

print "Job done."