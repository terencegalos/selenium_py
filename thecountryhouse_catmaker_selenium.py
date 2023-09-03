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
URL = "https://www.thecountryhouse.com/site_map.asp"
items = []

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser
    
def init_login(driver,un,pw):    
    driver.get(URL)
    # try:
        # print "Logging in..."
        # driver.find_element_by_id('logonUsername').send_keys(un)
        # driver.find_element_by_id('logonPassword').send_keys(pw)
        # driver.find_element_by_name('B1').click()

        # print ("Login Success.")
    # except:
        # print "Login failed."
		
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

#get sitemap nav
nav  = br.find_elements_by_css_selector("#content > table > tbody > tr > td")
for x in range(len(nav)):
	if x > 0: # go to product nav directly
		n = br.find_elements_by_css_selector("#content > table > tbody > tr > td")[x]
		
		subnav = n.find_elements_by_css_selector("strong a")[:-1]		
		for s in range(len(subnav)):
			n = br.find_elements_by_css_selector("#content > table > tbody > tr > td")[x]
			cat = n.find_elements_by_css_selector("strong a")[:-1][s].text
			sublink = n.find_elements_by_css_selector("strong a")[:-1][s].get_attribute("href")
			
			print cat
			br.get(sublink)
			time.sleep(1)
			
			try:
				br.find_element_by_css_selector("#content > div > p > select > option:nth-child(4)").click() # show all
			except:
				print "No item found."
				br.get(URL)
				time.sleep(1)
				continue
			time.sleep(1)
			
			items = [a.get_attribute("href") for a in br.find_elements_by_css_selector("#content > div > div > p > a")]
			# for i in range(len(items)):
			for i in items:
				# br.get(br.find_elements_by_css_selector("#content > div > div > p > a")[i].get_attribute("href"))
				br.get(i)
				time.sleep(1)
				while True:
					try:
						sku = br.find_element_by_css_selector("#content > div.productPage > div.productDetails > p:nth-child(1)").text.splitlines()[1]
						print [sku,cat]
						table.append([sku,cat])
						break
					except:
						br.refresh()
						time.sleep(1)
						continue
				
				# go back to items view
				# br.back()
				# time.sleep(1)
		
			# go to homepage
			br.get(URL)
			time.sleep(1)


		
	
outfile = open('./csv/outfile/thecountryhouse_cat_results.csv','wb')
writer = csv.writer(outfile)
writer.writerows(table)

print "Job done."