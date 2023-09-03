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



url = "http://whdfloral.com/"
uname = "rick@waresitat.com"
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    br.get("http://barncandles.americommerce.com/")
    time.sleep(1)
    btn = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#utilnav ul li:nth-child(2) font b a")))
    btn.click()
    time.sleep(1)
    print "Logging in."
   
    driver.find_element_by_name("txtEmailAddress").send_keys(un)
    driver.find_element_by_name("txtPassword").send_keys(pw)
    driver.find_element_by_name("btnSignIn").click()
    time.sleep(5)
    print "Logged in."
	
	
def get_info(driver,out):
	name = WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.product-name > h1"))).text.encode("utf-8")
	sku = driver.find_element_by_css_selector("#product_addtocart_form > div.row > div.product-shop.col-sm-12.col-md-7.col-sms-6.col-smb-12 > h5").text.split()[2]
	image = driver.find_element_by_css_selector("a.cloud-zoom").get_attribute("href")
	ls = []
	ls.append(name)
	ls.append(sku)
	ls.append(image)
	print ls
	out.append(ls)
			
        
br = init_driver()
br.get(url)
time.sleep(1)
# btn = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ctl37_rpLinkList_ctl00_dvHorizontalNavItem a")))
# btn.click()
# time.sleep(2)


items = []
table = []
    


with open("./csv/infile/whd.csv","rb") as infile:
    for i in infile:
		while True:
			try:
				br.find_element_by_name("q").clear()
				br.find_element_by_name("q").send_keys(i)
				print "Searching for " + str(i)
				time.sleep(1)
				break
			except:
				br.get(url)
				time.sleep(1)
				continue
		try:
			item = [i.get_attribute("href") for i in br.find_elements_by_css_selector("h2.product-name a")]
			time.sleep(1)
			for i in item:
				print i
				items.append(i)
		except:
			print "No item found. Searching for next item..."

print "All items now ready to scraped.**"            

for i in set(items):
	print "Navigating to " + str(i)
	br.get(i)
	time.sleep(1)
	while True:
		try:
			get_info(br,table)
			break
		except Exception as e:
			br.refresh()
			print e
			time.sleep(1)
			continue

print "**Job Done***"    
    
        
outfile = open("./csv/outfile/whd_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table) 