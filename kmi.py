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

login = "http://floralkmi.com/"
uname = "waresitat"
passw = "wolfville"
url = "http://floralkmi.com/index.php?option=com_virtuemart&Itemid=95"

    
def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    driver.get(login)
    print "Logging in."
    try:
        driver.find_element_by_name("username").send_keys(un)
        driver.find_element_by_name("passwd").send_keys(pw)
        driver.find_element_by_name("Submit").click()
        time.sleep(5)
        print "Logged in."
    except:
        print "Log in failed."
		
def get_info(driver,out):
	ls = []
	desc = driver.find_element_by_class_name("description").text.encode("utf-8")
	sku = driver.find_element_by_class_name("product_name").text.encode("utf-8")
	try:
		qty1 = driver.find_element_by_css_selector("tr.sectiontableentry1:nth-child(1) td:nth-child(1)").text.encode("utf-8").split("-")[0]
	except:
		qty1 = ""
	try:
		price1 = driver.find_element_by_css_selector("tr.sectiontableentry1:nth-child(1) td:nth-child(2)").text.encode("utf-8")
	except:
		price1 = ""
	try:
		qty3 = driver.find_element_by_css_selector("tr:nth-child(3) td:nth-child(1)").text.encode("utf-8").split("-")[0]
	except:
		qty3 = ""
	try:
		price3 = driver.find_element_by_css_selector("tr:nth-child(3) td:nth-child(2)").text.encode("utf-8")
	except:
		price3 = ""
	try:
		qty2 = driver.find_element_by_css_selector("tr.sectiontableentry2 td:nth-child(1)").text.encode("utf-8").split("-")[0]
	except:
		qty2 = ""
	try:
		price2 = driver.find_element_by_css_selector("tr.sectiontableentry2 td:nth-child(2)").text.encode("utf-8")
	except:
		price2 = ""
	try:
		image = br.find_element_by_css_selector("div.browseProductImage.Fly a").get_attribute("href")
	except:
		image = br.find_element_by_css_selector("#vmMainPage div.Product-border div div:nth-child(1) div.float-left div div img").get_attribute("src")
	ls.append(sku)
	ls.append(desc)
	ls.append(qty1)
	ls.append(price1)
	ls.append(qty2)
	ls.append(price2)
	ls.append(qty3)
	ls.append(price3)
	ls.append(image)
	out.append(ls)
	print ls

br = init_driver()
init_login(br,uname,passw)

br.get(url)
time.sleep(1)

table = []
with open("./csv/infile/kmi.csv","rb") as infile:
    for i in infile:
		print "Searching for item: " +str(i)
		WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "keyword"))).clear()
		br.find_element_by_id("keyword").send_keys(i)
		time.sleep(1)
		try:
			get_info(br,table)
		except:
			attempt = 0
			while True:
				try:
					items = [it.get_attribute("href") for it in br.find_elements_by_css_selector("h2.browseProductTitle a.product_name")]
					for item in items:
						br.get(item)
						get_info(br,table)
					break
					attempt = 0
				except Exception as e:
					while attempt < 3:
						print e
						print attempt
						br.refresh()
						time.sleep(2)
						attempt = attempt + 1
						continue
					else:
						break
outfile = open("./csv/outfile/kmi1.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)            