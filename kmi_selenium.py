import time
import urllib
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException

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
	desc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#vmMainPage div.Product-border div div:nth-child(1) div.floatElement div.description"))).text.encode("utf-8")
	print desc
	sku = driver.find_element_by_class_name("product_name").text.encode("utf-8")
	print sku
	try:
		minqty = driver.find_element_by_css_selector("#vmMainPage div.Product-border div div:nth-child(1) div.floatElement div.product-divider div.browsePriceContainer table tbody tr:nth-child(1) td:nth-child(1)").text.encode("utf-8")
	except:
		minqty = ""
	print minqty
	try:
		price1 = driver.find_element_by_css_selector("#vmMainPage div.Product-border div div:nth-child(1) div.floatElement div.product-divider div.browsePriceContainer table tbody tr:nth-child(1) td:nth-child(2)").text.encode("utf-8")
	except:
		price1 = ""
	print price1
	
	try:
		qty2 = driver.find_element_by_css_selector("#vmMainPage div.Product-border div div:nth-child(1) div.floatElement div.product-divider div.browsePriceContainer table tbody tr.sectiontableentry2 td:nth-child(1)").text.encode("utf-8")
		price2 = driver.find_element_by_css_selector("#vmMainPage div.Product-border div div:nth-child(1) div.floatElement div.product-divider div.browsePriceContainer table tbody tr.sectiontableentry2 td:nth-child(2)").text.encode("utf-8")
	except:
		qty2 = ""
		price2 = ""
	try:
		qty3 = driver.find_element_by_css_selector("#vmMainPage div.Product-border div div:nth-child(1) div.floatElement div.product-divider div.browsePriceContainer table tbody tr:nth-child(3) td:nth-child(1)").text.encode("utf-8")
		price3 = driver.find_element_by_css_selector("#vmMainPage div.Product-border div div:nth-child(1) div.floatElement div.product-divider div.browsePriceContainer table tbody tr:nth-child(3) td:nth-child(2)").text.encode("utf-8")
	except:
		qty3 = ""
		price3 = ""
		
	print qty2, price2, qty3, price3
	try:
		image = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.browseProductImage.Fly a"))).get_attribute("href")
	except:
		image = "No image."
	ls.append(sku)
	ls.append(desc)
	ls.append(minqty.split("-")[0].strip())
	ls.append(price1)
	ls.append(qty2.split("-")[0].strip())
	ls.append(price2)
	ls.append(qty3.split("-")[0].strip())
	ls.append(price3)
	ls.append(image)
	table.append(ls)
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
		except Exception as e:
			print e
			time.sleep(1)
			try:
				items = [it.get_attribute("href") for it in br.find_elements_by_css_selector("a.product_name")]
				for item in set(items):
					br.get(item)
					time.sleep(1)
					get_info(br,table)
			except:
				print "Item not found."


outfile = open("./csv/outfile/kmi_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()