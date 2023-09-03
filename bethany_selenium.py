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

login = "http://bethanylowe.com/login"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    driver.get(login)
    print "Logging in."
    try:
        driver.find_element_by_name("log").send_keys(un)
        driver.find_element_by_name("pwd").send_keys(pw)
        driver.find_element_by_name("wp-submit").click()
        time.sleep(5)
        print "Success."
    except:
        print "Log in failed."
        driver.close()
def get_info(driver,out):
	ls = []
	#sku = driver.find_element_by_css_selector("span.cart-number").text.split()[-1:]
	sku = driver.find_element_by_css_selector("span.cart-number").text.encode("utf-8")
	print sku
	min = driver.find_element_by_css_selector("div.cart-content > label > input").get_attribute("value")
            
	# WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#page article a img"))).click()
	# time.sleep(2)
	dim = driver.find_element_by_css_selector("body > div.middle-section > div > div > article > div > form > div.col-sm-7.cart-text-area > div.cart-content > p")
	image = driver.find_element_by_css_selector("body > div.middle-section > div > div > article > div > form > div.col-sm-5 > a > img").get_attribute("src")
	
	ls.append((sku.split()[-1:])[0])
	ls.append(min)
	ls.append(dim.text.encode("utf-8"))
	ls.append(image)
	out.append(ls)
	print ls

br = init_driver()
init_login(br,uname,passw)
table = []
with open("./csv/infile/bethanylowe.csv","rb") as infile:
	for i in infile:
		ls = []
		print "Searching for item: " + str(i)
		br.find_element_by_id("s").clear()
		br.find_element_by_id("s").send_keys(i)
		time.sleep(2)
		try:
			get_info(br,table)
		except Exception as e:
			print e
			time.sleep(1)
			print "No item found. Searching next item..."

print "***Job Done***"        
        
outfile = open("./csv/outfile/bethanylowe_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()