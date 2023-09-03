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

url = "https://thehearthsidecollection.com/"
uname = "service@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):
	driver.get(url)
	time.sleep(1)
	driver.find_element_by_css_selector("#sw_dropdown_278 a span").click()
	time.sleep(1)
	driver.find_element_by_css_selector("#account_info_278 div.ty-account-info__buttons.buttons-container a.cm-dialog-opener.cm-dialog-auto-size.ty-btn.ty-btn__secondary").click()
	time.sleep(1)
	try:
		print "Logging in..."
		# driver.find_element_by_id('login_').send_keys(un)
		ActionChains(driver).move_to_element(driver.find_element_by_css_selector("#login_block278 div div form")).perform()
		WebDriverWait(br, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#login_popup278"))).send_keys(un)
		driver.find_element_by_css_selector('#psw_popup278').send_keys(pw)
		driver.find_element_by_name("dispatch[auth.login]").click()
		print "Success."
		time.sleep(3)
	except:
		print "Login failed."
		br.close()
def get_info(driver,out):
	ls = []
	try:
		title = driver.find_element_by_css_selector("h1.ty-product-block-title").text.encode("utf-8")
	except:
		title = "No title."
	try:
		sku = driver.find_element_by_css_selector("span.ty-control-group__item").text.encode("utf-8")
	except:
		sku = "No SKU."
	try:
		section = driver.find_element_by_css_selector("div.ty-breadcrumbs.clearfix").text.encode("utf-8")
	except:
		section = "No section."
	try:
		price = driver.find_element_by_css_selector("span.ty-price-num").text.encode("utf-8")
	except:
		price = "No price."
	try:
		desc = driver.find_element_by_css_selector("#content_description div p").text.encode("utf-8")
	except:
		desc = "No desc."
	try:
		image = driver.find_element_by_css_selector("img.ty-pict").get_attribute("src")
	except:
		image = "No image."
	
	ls.append(title)
	ls.append(sku)
	ls.append(section)
	ls.append(price)
	ls.append(desc)
	ls.append(image)
	out.append(ls)
	print ls
		
br = init_driver()
init_login(br,uname,passw)

items = []
table = []      
with open("./csv/infile/hearthside.csv","rb") as infile:
    for i in infile:
		try:
			print "Searching for item: " + str(i)
			br.find_element_by_name("hint_q").clear()
			br.find_element_by_name("hint_q").send_keys(i)
			time.sleep(1)
		except:
			try:
				br.find_element_by_name("q").clear()
				br.find_element_by_name("q").send_keys(i)
				time.sleep(1)
			except:
				print "Item not found."
		try:
			item = [it.get_attribute("href") for it in br.find_elements_by_css_selector("div.ty-grid-list__item-name a")]
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
				
outfile = open("./csv/outfile/hearthside_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()