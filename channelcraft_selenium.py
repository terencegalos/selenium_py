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

url = "http://channelcraft.com/Scripts/PublicSite/"
user = "waresitat"
pw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser
 
def init_login(u,p,d):
	d.find_element_by_name("username").send_keys(u)
	d.find_element_by_name("password").send_keys(p)
	d.find_element_by_css_selector("#loginWrapper > tbody > tr:nth-child(2) > td:nth-child(1) > form > table > tbody > tr:nth-child(3) > td:nth-child(2) > input").click()
	time.sleep(1)
	print "Login success."

br = init_driver() 
time.sleep(1)
br.get(url)
time.sleep(1)
br.get("http://www.channelcraft.com/Wholesale-Login/")
time.sleep(1)
init_login(user,pw,br)



table = []
with open("./csv/infile/channelcraft.csv","rb") as infile:
	for i in infile:
		ls = []
		try:
			print "Searching for item: " + i
			br.find_element_by_name("term").clear()
			br.find_element_by_name("term").send_keys(i)
			time.sleep(1)
			link = br.find_element_by_css_selector("#product > div > a").get_attribute("href")
			br.get(link)
			time.sleep(1)
			ls.append((br.find_element_by_css_selector("#descCell > p.sku").text.encode("utf-8")).split()[1])
			ls.append(br.find_element_by_css_selector("#descCell > p.desc").text.encode("utf-8"))
			ls.append(br.find_element_by_css_selector("#imgCell > img").get_attribute("src"))
			print ls
			table.append(ls)
			br.back()
			time.sleep(1)
		except:
			print "No item found. Getting next item..."
			
			
outfile = open("./csv/outfile/channelcraft.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()