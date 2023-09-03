from selenium import webdriver
import time
import urllib
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv

url = "https://www.thecountryhouse.com/search.asp?action=search"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
 

br = init_driver() 
time.sleep(1)
br.get(url)
time.sleep(12)



table = []
with open("./csv/infile/countryhouse_infile.csv","rb") as infile:
	for i in infile:
		br.get(url)
		ls = []
		try:
			print "Searching for item: " + i
			br.find_element_by_css_selector("#content  form  input.searchField").clear()
			br.find_element_by_css_selector("#content  form  input.searchField").send_keys(str(i))
			time.sleep(1)
			sku = WebDriverWait(br, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content div.productPage div.productDetails p:nth-child(1)")))
			print sku.text
			image = WebDriverWait(br, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content div.productPage div.productImg img")))                  
			print [image.get_attribute("src")]
			ls.append(sku.text) 
			ls.append(image.get_attribute("src"))
			print ls
			table.append(ls)
		except:
			print "No item found. Getting next item..."

outfile = open("./csv/outfile/thecountryhouse_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()