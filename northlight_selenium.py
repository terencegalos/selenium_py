from selenium import webdriver
import time
import urllib2
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains
from urllib import urlopen
import urllib
import csv

url = "http://northlightseasonal.com/"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):
	driver.get("https://northlightseasonal.com/account/login")
	time.sleep(1)
	print "Logging in.."
	
	driver.find_element_by_name("customer[email]").send_keys(un)
	driver.find_element_by_name("customer[password]").send_keys(pw)
	driver.find_element_by_css_selector("#customer_login div.action_bottom p input").click()
	time.sleep(5)
	
def get_info(driver,out):
	ls = []
	try:
		title = driver.find_element_by_css_selector("div#content h1").text.encode("utf-8")
	except:
		title = "No title."
	try:
		price = driver.find_element_by_css_selector("div#price-field").text.encode("utf-8")
	except:
		price = "No price."
	try:
		desc = driver.find_element_by_css_selector("div.description").text.encode("utf-8")
	except:
		desc = "No desc."
	try:
		image = driver.find_element_by_css_selector("div.main a").get_attribute("href")
	except:
		image = "No image."
	
	ls.append(title)
	ls.append((desc.split("\n")[-2:]).split(",")[0])
	ls.append(price)
	ls.append(desc)
	ls.append(image)
	out.append(ls)
	print ls
		
br = init_driver()
init_login(br,uname,passw)

items = []
table = []      
with open("./csv/infile/northlight.csv","rb") as infile:
    for i in infile:
		print "Searching for item: " + str(i)
		br.find_element_by_name("q").clear()
		br.find_element_by_name("q").send_keys(i)
		time.sleep(1)
		try:
			item = [it.get_attribute("href") for it in br.find_elements_by_css_selector("ol.searchresults li h3 a")]
			for i in item:
				print "Navigating to " + i
				br.get(i)
				time.sleep(1)
				get_info(br,table)
		except Exception as e:
			print e
			try:
				get_info(br,table)
			except:
				print "Item not found."
				
outfile = open("./csv/outfile/northlight_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()