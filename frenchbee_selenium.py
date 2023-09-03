from selenium import webdriver
import time
import urllib
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from urllib2 import urlopen
import csv

uname = "service@waresitat.com"
pw = "wolfville"
url = "http://www.thefrenchbee.com/floral.html"

def init_driver():
	path = "./chrome_driver/chromedriver"
	browser = webdriver.Chrome(executable_path = path)
	browser.wait = WebDriverWait(browser,5)
	return browser
    
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]
    
def init_login(driver,un,passw):    
	driver.get(url)
	try:
		print "Logging in..."
		WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "ctl00_PageContent_EMail"))).send_keys(un)
		WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "ctl00_PageContent_txtPassword"))).send_keys(pw)
		btn = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "ctl00_PageContent_LoginButton")))
		btn.click()
		print "Login Success."
	except:
		print "Login failed."
		
br = init_driver()
br.get(url)
links = [c.get_attribute("href") for c in br.find_elements_by_css_selector("body table tbody tr td table tbody tr:nth-child(2) td:nth-child(2) table tbody tr:nth-child(5) td:nth-child(2) table tbody tr td a")]

table = []
items = []
for i in range(1,len(links)):
	print "Navigating to: " + links[i]
	try:
		br.get(links[i])
		time.sleep(1)
		[items.append(it.get_attribute("href")) for it in br.find_elements_by_css_selector("body table tbody tr td table tbody tr:nth-child(2) td:nth-child(2) table tbody tr:nth-child(7) td:nth-child(3) table tbody tr td a")]
	except:
		pass

for item in items:
	while True:
		try:
			br.get(item)
			time.sleep(1)
			break
		except:
			br.refresh()
			continue
	print "Item page loaded."
	ls = []
	try:
		name = br.find_element_by_css_selector("body table tbody tr td table tbody tr:nth-child(2) td:nth-child(2) table tbody tr:nth-child(5) td:nth-child(2) table tbody tr:nth-child(2) td").text.encode("utf-8")
		dim = br.find_element_by_css_selector("body table tbody tr td table tbody tr:nth-child(2) td:nth-child(2) table tbody tr:nth-child(5) td:nth-child(2) table tbody tr:nth-child(3) td").text.encode("utf-8")
		image = br.find_element_by_css_selector("body table tbody tr td table tbody tr:nth-child(2) td:nth-child(2) table tbody tr:nth-child(5) td:nth-child(2) table tbody tr:nth-child(1) td p img").get_attribute("src")
	
		ls.append(name)
		ls.append(item)
		ls.append(dim)
		ls.append(image)
		print ls
		table.append(ls)
	except:
		pass
    
outfile = open("./csv/outfile/frenchbee_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)