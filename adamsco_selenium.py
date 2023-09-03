from selenium import webdriver
import time
import urllib2
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from urllib import urlopen
import urllib
import csv

login = "https://adamsandco.net/home.php"
url = "http://www.cwpeale.com/"
uname = "salesrep"
passw = "adams"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):    
    driver.get(login)
    time.sleep(6)
    print "Logging in..."
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#header div ul li:nth-child(1) a"))).click()
    time.sleep(1)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,"username"))).send_keys(un)
    driver.find_element_by_name('password').send_keys(pw)
    driver.find_element_by_css_selector("input.formbutton").click()
    print "Login Success."
    time.sleep(10)
    # except:
        # print "Login failed."
def get_info(driver,out):
	ls = []
	name = driver.find_element_by_css_selector("body div.product.container div div:nth-child(1) div.summary.col-tablet-7 h1").text.encode("utf-8")
	print name
	try:
		image = driver.find_element_by_css_selector("#main_image img:nth-child(1)").get_attribute("src")
		print image
	except:
		image = "No image."
	
	ls.append(name)
	#skip instead if no image label
	print image.split("/")[-1:][0]
	if( "adams_no_image" in image.split("/")[-1:][0]):
		print "No image label found."
		return
	ls.append(image)
	
	try:
		rows = driver.find_elements_by_css_selector("body div.product.container div div tbody tr")
		for row in rows:
			info = row.find_elements_by_css_selector("td")
			data = "|".join([i.text for i in info])
			ls.append(data)
		print ls
		out.append(ls)
	except Exception as e:
		raise e
		print "No table found."
		print ls
		out.append(ls)
            

#initialize and open browser
br = init_driver()
br.get("https://adamsandco.net/")
time.sleep(1)

items = []
table = []

with open("./csv/outfile/noimg/Adams_and_Company.csv","rb") as infile:
	for i in infile:
		try:
			print "\nSearching for item " + str(i)
			br.find_element_by_name("query").clear()
			br.find_element_by_name("query").send_keys(i.split(",")[1])
			time.sleep(1)
			get_info(br,table)
		except NoSuchElementException:
			print "Name not found."
			print "Clicking item..."
			time.sleep(2)
			try:
				br.find_element_by_css_selector("body div.category.container div div.products.list.col-tablet-9 div.product.container-fluid div div.summary.col-tablet-8.col-phone-7 div a").click()
				time.sleep(1)
				get_info(br,table)
			except Exception as a:
				print a
				time.sleep(1)
				print "Item not found."

outfile = open("./csv/outfile/adamsco_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()           