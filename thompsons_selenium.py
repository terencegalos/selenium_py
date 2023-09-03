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



url = "http://www.thompsonscandle.com/newproducts.aspx"
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
	
	
def get_more_info(driver,list,out):
	cat = driver.find_element_by_css_selector("div.breadcrumb").text.encode("utf-8")
	pic = driver.find_element_by_css_selector("#Zoomer").get_attribute("href")
	list.append(cat)
	list.append(pic)
	out.append(list)
	print list
	
def get_info(driver,out):
	name = WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-detail-div h1"))).text.encode("utf-8")
	
	try:
		sku = driver.find_element_by_css_selector("#product-detail-div table.prod-detail tbody tr:nth-child(1) td.prod-detail-rt div.prod-detail-part span.prod-detail-part-value").text.encode("utf-8")
		try:
			option = "|".join([t.text.encode("utf-8") for t in br.find_elements_by_css_selector("div.variationDropdownPanel select option")])
		except:
			option = "No option."
		ls = []
		ls.append(name)
		ls.append(sku)
		ls.append(option)
		get_more_info(driver,ls,out)
	except:
		option = br.find_elements_by_css_selector("div.variationDropdownPanel select option")
		for x in range(1,len(option)):
			ls = []
			ls.append(name)
			br.find_elements_by_css_selector("div.variationDropdownPanel select option")[x].click()
			time.sleep(3)
			sku = driver.find_element_by_css_selector("#product-detail-div table.prod-detail tbody tr:nth-child(1) td.prod-detail-rt div.prod-detail-part span.prod-detail-part-value").text.encode("utf-8")
			ls.append(sku)
			opt = br.find_elements_by_css_selector("div.variationDropdownPanel select option")[x].text.encode("utf-8")
			ls.append(opt)
			get_more_info(driver,ls,table)
			
        
br = init_driver()
br.get(url)
time.sleep(3)
# btn = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ctl37_rpLinkList_ctl00_dvHorizontalNavItem a")))
# btn.click()
# time.sleep(2)


items = []
table = []
    


with open("./csv/infile/thompsons_file.csv","rb") as infile:
    for i in infile:
		while True:
			try:
				br.find_element_by_name("ctl00$ctl03$search").clear()
				br.find_element_by_name("ctl00$ctl03$search").send_keys(i)
				print "Searching for " + str(i)
				time.sleep(1)
				break
			except:
				br.refresh()
				time.sleep(1)
				continue
		try:
			item = br.find_elements_by_css_selector("tbody tr td.product-list-item-container div div h5 a")
			time.sleep(1)
			for i in item:
				itm = i.get_attribute("href")
				print itm
				items.append(itm)
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
    
        
outfile = open("./csv/outfile/thompsonscandle_output2.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table) 