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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


url = "http://www.millerdecor.com/index.html"
uname = "rick@waresitat.com"
passw = "Inspire2day"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser
    
def init_login(driver,un,pw):
    br.get("http://www.millerdecor.com/page/password/8985573.htm")
    time.sleep(1)
    print "Logging in."
    
    #driver.find_element_by_name("email_address").send_keys(un)
    driver.find_element_by_name("password").send_keys(pw)
    driver.find_element_by_name("password").send_keys(Keys.ENTER)
    # driver.find_element_by_css_selector("body > div > div.theme-page > div.theme-content > form > p:nth-child(2) > input[type=\"submit\"]:nth-child(2)").click()
    time.sleep(1)
    print "Success."
	
def get_info(driver,link,out,it):
    print "Getting attributes for item " + str(link)
    driver.get(link)
    time.sleep(1)
    try:
		name = driver.find_element_by_css_selector("#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > font:nth-child(2) > strong > div").text.encode("utf-8")
    except:
		name = ""
    try:
		sku = it
    except:
		sku = ""
    # cat = "|".join([i.text.encode("utf-8") for i in driver.find_elements_by_css_selector("#breadcrumbs > li")])
    cat = driver.find_element_by_css_selector("#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > font:nth-child(1) > a").text.encode("utf-8")
    try:
		stock = driver.find_element_by_css_selector("#availability").text.encode("utf-8")
    except:
		stock = ""
    try:
		price = driver.find_element_by_css_selector("#price > strong").text.encode("utf-8")
    except:
		price = ""
    try:
        image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > div > p:nth-child(10) > img")))
        image = image.get_attribute("src")
    except:
        image = "none"
    ls = []
    ls.append(name)
    ls.append(sku)
    ls.append(cat)
    ls.append(stock)
    ls.append(price)
    ls.append(image)
    print ls
    out.append(ls)
	

    
    
####################################################################################################################################################################################################################################
    
                
br = init_driver()
init_login(br,uname,passw)
time.sleep(1)

cats = [link.get_attribute("href") for link in br.find_elements_by_css_selector("#colTable > tbody > tr> td > p > a")]
print cats
print "Waiting for homepage to load..."
time.sleep(1)

items = []
table = []

for cat in cats:
    if "http" not in cat:
        continue
		
    print "Navigating to " + cat
    br.get(cat)
    time.sleep(1)
	
    try:
        dim = br.find_element_by_css_selector("#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > p:nth-child(6) > span:nth-child(1) > strong").text.encode("utf-8")
    except:
        dim = "No dim."
    
	item = [it.get_attribute("href") for it in br.find_elements_by_css_selector("#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > div > table > tbody > tr > td > div > a")]
    for t in item:
        print t
        items.append(t)
    
	while True:
		try:
			br.find_element_by_link_text("Next >").click()
			print "Loading next page.."
			time.sleep(1)
			item = [it.get_attribute("href") for it in br.find_elements_by_css_selector("#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > div > table > tbody > tr > td > div > a")]
			for t in item:
				print t
				items.append(t)
		except:
			print "Page exhausted"
			break
            
            
for i in items:
	print i
	br.get(i)
	time.sleep(1)
	try:
		# get_info(br,i,table,sk)
		choice = br.find_elements_by_css_selector("select > option")
		for c in range(len(choice)):
			sk = driver.find_element_by_css_selector("#code").text.encode("utf-8")
			br.find_elements_by_css_selector("select > option")[c].click()
			time.sleep(1)
			get_info(br,i,table,sk)
	except:
		sk = br.find_element_by_css_selector("#code").text.encode("utf-8")
		get_info(br,i,table,sk)
		
print "***Job Done***"
              
        
        
outfile = open("./csv/outfile/miller_decor_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()