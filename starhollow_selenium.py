from selenium import webdriver
import time
import urllib
import requests
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains


url = "http://starhollow.com/index.php?route=common/home"
login = "http://starhollow.com/index.php?route=account/login"
destination = "https://www.waresitat.com/vendor_detail.cfm?VendorID=7947"
uname = "rick@waresitat.com"
passw = "wolfville"


def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser
    
def init_login(driver,un,pw):
	driver.get(login)
	time.sleep(1)
	driver.find_element_by_name("email").send_keys(un)
	driver.find_element_by_name("password").send_keys(pw)
	driver.find_element_by_css_selector("#content div.login-content div.right form div input.button").click()
	time.sleep(5)
	print "Logged in."


        
br = init_driver()
init_login(br,uname,passw)
time.sleep(1)

items = []
table = []
cats = []

print "Search items from list."
with open("./csv/infile/starhollow_infile.csv","rb") as infile:
	for i in infile:
		br.find_element_by_name("search").clear()
		br.find_element_by_name("search").send_keys(i)
		time.sleep(2)
		try:
			item = br.find_elements_by_css_selector("#content div.product-grid div div.image a")
			for it in item:
				itm = it.get_attribute("href")
				print itm
				items.append(itm)
		except:
			print "Item not found."

print "***Done searching***"			
			
for item in items:
	br.get(item)
	time.sleep(2)
	desc = br.find_element_by_css_selector("#tab-information div.description").text.encode("utf-8")
	optxt = br.find_elements_by_css_selector("table tbody tr td label img")
	optimg = br.find_elements_by_css_selector("table tbody tr td label img")
	
	for x in range(len(optxt)-1):
		ls = []
		code = desc.split()
		style = optxt[x].get_attribute("alt")
		try:
			pic = optimg[x].get_attribute("src")
		except:
			pic = "No image."
		
		ls.append(code[2])
		ls.append(style)
		ls.append(pic)
		
		table.append(ls)
		print ls

print "**Job Done***"

outfile = open("./csv/outfile/starhollow_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table) 