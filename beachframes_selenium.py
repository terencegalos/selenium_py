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

login = "https://www.kkinteriors.com/login"
uname = "service@waresitat.com"
passw = "wolfville"
url = "http://www.beachframes.com/"

    
def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    driver.get(login)
    print "Logging in."
    try:
        driver.find_element_by_id("Username").send_keys(un)
        driver.find_element_by_id("Password").send_keys(pw)
        driver.find_element_by_css_selector("input.button").click()
        time.sleep(5)
        print "Logged in."
    except:
        print "Log in failed."

br = init_driver()
br.get(url)
time.sleep(1)

table = []
with open("./csv/infile/beachframes.csv","rb") as infile:
    for i in infile:
		print "\nSearching for item: " +str(i) + "\n"
		while True:
			try:
				WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "search"))).clear()
				br.find_element_by_id("search").send_keys(i)
				br.find_element_by_css_selector("#search_mini_form button").click()
				time.sleep(1)
				break
			except:
				br.refresh()
				time.sleep(1)
				continue
		try:
			ls = []
			item = WebDriverWait(br, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2.product-name a"))).get_attribute("href")
			print "\n***Item found***\n"
			print "Navigating to item: " + str(item) + "\n"
			br.get(item)
			time.sleep(1)

			name = br.find_element_by_css_selector("div.product-name h1").text.encode("utf-8")
			time.sleep(1)
			image = br.find_element_by_css_selector("#image").get_attribute("src")
			ls.append(name)
			ls.append(name.split("(")[1])
			ls.append(image)
			table.append(ls)
			print ls
		except:
			if br.find_elements_by_css_selector("h2.product-name a"):
				items = br.find_elements_by_css_selector("h2.product-name a")
				for item in items:
					itm  = item.get_attribute("href")
					print "Navigating to item: " + str(itm) + "\n"
					br.get(itm)
					time.sleep(1)
					name = br.find_element_by_css_selector("div.product-name h1").text.encode("utf-8")
					time.sleep(1)
					image = br.find_element_by_css_selector("#image").get_attribute("src")
					ls.append(name)
					ls.append(name.split("(")[1])
					ls.append(image)
					table.append(ls)
					print ls
			else:
				print "Item not found."
	
outfile = open("./csv/outfile/beachframes.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)        