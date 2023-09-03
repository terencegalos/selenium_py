
from selenium import webdriver
import time
import urllib
import requests
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains


login = "http://kraftklub.com/myaccount.php"
url = "http://kraftklub.com/index.html"
uname = "kaye.williams@waresitat.com"
passw = "b2bonline"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    br.get(login)
    time.sleep(1)
    print "Logging in."
    
    driver.find_element_by_name("email").send_keys(un)
    driver.find_element_by_name("password").send_keys(pw)
    driver.find_element_by_id("greenbttn3").click()
    time.sleep(5)	
    print "Logged in."

def get_info(driver,link,out):
	print "Navigating to: \n" + str(link)
	driver.get(link)
	time.sleep(1)
	sku = driver.find_element_by_css_selector("#right > div.detail > div:nth-child(2) > div > p:nth-child(2)").text.split()[0]
	try:
		desc = driver.find_element_by_css_selector("#right > div.detail > div:nth-child(2) > div > p:nth-child(5)").text.encode("utf-8")
	except:
		desc = "No desc."
	cat = driver.find_element_by_css_selector("#location").text.encode("utf-8")  
	try:
		sale = driver.find_element_by_css_selector("#right > div.detail > div:nth-child(2) > div > table > tbody > tr:nth-child(1) > td:nth-child(3)").text.encode("utf-8")
	except:
		sale = "No sale."
	try:
		tier1qty = driver.find_element_by_css_selector("#qty1 > option:nth-child(1)").get_attribute("value")
	except:
		tier1qty = "No tier 1 qty."
	try:
		tier2qty = driver.find_element_by_css_selector("#qty2").get_attribute("value")
	except:
		tier2qty = "No tier 2 qty."
	try:
		tier3qty = driver.find_element_by_css_selector("#qty3").get_attribute("value")
	except:
		tier3qty = "No tier 3 qty."
	
	tier1price = driver.find_element_by_css_selector("#right > div.detail > div:nth-child(2) > div > table > tbody > tr:nth-child(1) > td:nth-child(2)").text.encode("utf-8")
	
	try:
		tier2price = driver.find_element_by_css_selector("#right > div.detail > div:nth-child(2) > div > table > tbody > tr:nth-child(2) > td:nth-child(2)").text.encode("utf-8")
	except:
		tier2price = "No tier 2 price."
	try:
		tier3price = driver.find_element_by_css_selector("#right > div.detail > div:nth-child(2) > div > table > tbody > tr:nth-child(3) > td:nth-child(2)").text.encode("utf-8")
	except:
		tier3price = "No tier 2 price."
	try:
		dim = desc.split()[-1:]
	except:
		dim = "No dimension available."
	try:
		image = driver.find_element_by_css_selector("#zoom1").get_attribute("href")
	except:
		image = "No image."
	ls = []
	ls.append(sku)
	ls.append(desc)
	ls.append(cat)
	ls.append(sale)
	ls.append(tier1qty)
	ls.append(tier1price)
	ls.append(tier2qty)
	ls.append(tier2price)
	ls.append(tier3qty)
	ls.append(tier3price)
	ls.append(image)
	print ls
	out.append(ls)


    
    
####################################################################################################################################################################################################################################
    
                
br = init_driver()
init_login(br,uname,passw)
time.sleep(1)

#br.get("http://kraftklub.com/index.html")
br.get("http://kraftklub.com/products/new-products.html")
print "Waiting for homepage to load..."
time.sleep(1)


items = []
table = []
cats = []

# item = br.find_elements_by_css_selector("#right div:nth-child(2) div div.pic a")
# for i in item:
    # itm = i.get_attribute("href")
    # print itm
    # items.append(itm) 
# while True:
    # try:
        # br.find_element_by_link_text("Next").click()
        # print "Going to the next page for more items..."
        # time.sleep(1)
        # item = br.find_elements_by_css_selector("#right div:nth-child(2) div div.pic a")
        # for i in item:
            # itm = i.get_attribute("href")
            # print itm
            # items.append(itm) 
    # except:
        # print "No more items. Everything is in this page."
        # break

# lnks = br.find_elements_by_css_selector("#leftside div.menubox li a");
# links = []

# for i in lnks:
    # itm = i.get_attribute("href")
    # print itm
    # links.append(itm)

# for i in links:
    # print "Getting items in " + str(i)
    # br.get(i)          
    # time.sleep(1)
    # item = br.find_elements_by_css_selector("#right div:nth-child(2) div div.pic a")
    # for i in item:
        # itm = i.get_attribute("href")
        # print itm
        # items.append(itm) 
    # while True:
        # try:
            # br.find_element_by_link_text("Next").click()
            # print "Going to the next page for more items..."
            # time.sleep(1)
            # item = br.find_elements_by_css_selector("#right div:nth-child(2) div div.pic a")
            # for i in item:
                # itm = i.get_attribute("href")
                # print itm
                # items.append(itm) 
        # except:
            # print "No more items. Everything is in this page."
            # break
        
    
    

# print "All items scraped. Getting attributes for each..."   

# outfile1 = open("./csv/outfile/kraftklub_items.csv","wb")
# writer1 = csv.writer(outfile1)    
# writer1.writerow(items)        


# for i in items:
    # print "Navigating to " + str(i)
    # get_info(br,i,table) 

with open("./csv/infile/kraftklub_infile.csv","rb") as infile:
	for i in [line.rstrip() for line in infile]:
		print "Searching for " + i
		while True:
			try:
				br.find_element_by_name("searchWord").clear()
				br.find_element_by_name("searchWord").send_keys(i)
				br.find_element_by_name("searchWord").send_keys(Keys.ENTER)
				break
			except:
				br.refresh()
				time.sleep(1)
				continue
		try:
			time.sleep(1)
			link = br.find_element_by_css_selector("#right > div:nth-child(2) > div > div:nth-child(5) > a").get_attribute("href")
			print link
			items.append(link)
		except:
			print "Item not found."
			
for it in set(items):
	get_info(br,it,table)
		
print "***Job Done***"
              
        
        
outfile = open("./csv/outfile/kraftklub_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)