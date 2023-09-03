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

    
def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
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
table = []

br.get("http://www.lcpgifts.com/")
time.sleep(3)

table = []
with open("./csv/infile/lcpgifts.csv","rb") as infile:
    for i in infile:
		ls = []
		try:
			print "Searching for item: " + str(i)
			br.find_element_by_class_name("searchbar_textboxstyle").send_keys(i)
			time.sleep(1)
			sku = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sku")))
			cat = "|".join([i.text.encode("utf-8") for i in br.find_elements_by_css_selector("div#site_path a")])
			dim = br.find_element_by_class_name("size")
			try:
				verse = br.find_element_by_css_selector("#details > p.verse").text.encode("utf-8")
			except:
				verse = "No verse."
			image = br.find_element_by_xpath("//*[@id=\"content_asp_Repeater1_Image1_0\"]")
			ls.append(sku.text.encode("utf-8"))
			ls.append(cat.text.encode("utf-8"))
			ls.append(dim.text.encode("utf-8"))
			ls.append(verse)
			ls.append(image.get_attribute("src"))
			table.append(ls)
			print ls
			print "\n\n\n\n"
		except:            
			searches = br.find_elements_by_css_selector("div.image a")
			print "No item found. Search result found instead.\n\n\n"
			for search in searches:
				ls1 = []
				try:
					print search.text
					item = search.get_attribute("href")
					print "Navigating to: " + str(item)
					br.get(item)
					time.sleep(1)
					sku1 = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sku")))
					dim1 = br.find_element_by_class_name("size")
					image1 = br.find_element_by_xpath("//*[@id=\"content_asp_Repeater1_Image1_0\"]")
					ls1.append(sku1.text.encode("utf-8"))
					ls1.append(dim1.text.encode("utf-8"))
					ls1.append(image1.get_attribute("src"))
					table.append(ls1)
					print ls1
				except:
					continue
		else:
			continue


outfile = open("./csv/outfile/lighthouse_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)