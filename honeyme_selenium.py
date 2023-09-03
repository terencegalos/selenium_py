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

login = "http://www.honeyandme.com/shop/"
url = "http://www.honeyandme.com/"
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
        driver.find_element_by_name("username").send_keys(un)
        driver.find_element_by_name("password").send_keys(pw)
        driver.find_element_by_css_selector("#login_form div.sc_login button").click()
        time.sleep(8)
        print "Logged in."
    except:
        print "Log in failed."
        driver.close()
def get_info(driver,out):
	ls = []
	try:
		name = driver.find_element_by_css_selector("div.prod_main > div.prod_description > table > tbody > tr > td > table > tbody > tr:nth-child(1) > td")
	except:
		try:
			name = driver.find_element_by_css_selector("div.prod_main > div.prod_description > p > span:nth-child(1) > span > span")
		except:
			name = driver.find_element_by_css_selector("div.prod_main > div.prod_description > p > span:nth-child(2) > span > span")
	sku = name.text.encode("utf-8")
	sku = sku.split()[0]
	# WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#page article a img"))).click()
	# time.sleep(2)
	# dim = driver.find_element_by_css_selector("#page article div p:nth-child(2)")
	cat = "|".join([i.text.encode("utf-8") for i in driver.find_elements_by_css_selector("#sc_main > ul.breadcrumb_nav > li > a")])
	image = br.find_element_by_css_selector("div.prod_main div.prod_img_outer div a")
	ls.append(name.text.encode("utf-8"))
	ls.append(sku)
	ls.append(cat)
	ls.append(image.get_attribute("href"))
	out.append(ls)
	print ls
	
br = init_driver()
init_login(br,uname,passw)
time.sleep(1)
table = []
with open("./csv/infile/honeyme.csv","rb") as infile:
	for i in infile:
		ls = []
		print "Searching for item: " + str(i)
		br.find_element_by_name("search[terms]").send_keys(i)
		time.sleep(1)
		try:
			get_info(br,table)
		except:
			#try:
			item = [i.get_attribute("href") for i in br.find_elements_by_css_selector("div.prod_name > a")]
			for t in item:
				ls = []
				br.get(t)
				time.sleep(1)
				#try:
				get_info(br,table)
					# except Exception as e:
						# print "Error detected getting attributes. Check for errors."
						# print e
						# time.sleep(3)
						# continue
			# except:
				# print "Item not found."

print "***Job Done***"        
        
outfile = open("./csv/outfile/honeyme_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)