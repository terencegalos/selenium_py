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

login = "https://www.jonesrusticsigns.com/customer/account/login/"
url = "http://www.colorful-garden.com/"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    br.get(login)
    time.sleep(1)
    print "Logging in."
    
    driver.find_element_by_name("login[username]").send_keys(un)
    driver.find_element_by_name("login[password]").send_keys(pw)
    driver.find_element_by_name("send").click()
    time.sleep(5)
    print "Logged in."

def get_info(driver,link,out):
	print "Navigating to: \n" + str(link)
	driver.get(link)
	time.sleep(1)
	name = driver.find_element_by_css_selector("#add div.secondary h1").text.encode("utf-8")
	sku = driver.find_element_by_css_selector("#product_id").text.encode("utf-8")
	try:
		prodfeat = driver.find_element_by_css_selector("#add div.secondary div.productFeaturesBlock").text.encode("utf-8")
	except:
		prodfeat = "No prodfeat."
	time.sleep(1)
	desc = driver.find_element_by_css_selector("#tab-1 div").text.encode("utf-8")
	qty = driver.find_element_by_css_selector("#add div.secondary div:nth-child(7) div div div input").get_attribute("value")
	price = driver.find_element_by_id("price").text.encode("utf-8")
	try:
		image = driver.find_element_by_css_selector("#large").get_attribute("src")
	except:
		image = "No image."
	opt = [s.text for s in driver.find_elements_by_css_selector("#divOptionsBlock div.container div.opt-regular div.opt-field div.dropdown-format select option")]
	for x in range(len(opt)):
		ls = []
		ls.append(name)
		ls.append(sku)
		ls.append(desc)
		ls.append(prodfeat)
		ls.append(qty)
		ls.append(price)
		ls.append(image.replace("thumbnail.asp?file=",""))
		ls.append(opt[x])
		print ls
		out.append(ls)
		
def cat_scrape(driver,container):
	try:
		driver.find_element_by_link_text("View All").click()
		print "More items found. Loading all items..."
		time.sleep(1)
	except:
		print "All items are here."
	item = driver.find_elements_by_css_selector("div.name a")
	for it in item:
		i = it.get_attribute("href")
		print i
		container.append(i)

####################################################################################################################################################################################################################################
    
                
br = init_driver()
time.sleep(5)

br.get(url)
print "Waiting for homepage to load..."
time.sleep(1)

items = []
table = []
cats = []

# with open("./csv/infile/colorful-garden.csv","rb") as infile:
    # for i in infile:
		# while True:
			# try:
				# print "Searching for item " + i
				# br.find_element_by_name("keyword").clear()
				# br.find_element_by_name("keyword").send_keys(i)
				# time.sleep(1)
				# break
			# except:
				# print "Server overloaded."
				# br.find_element_by_css_selector("#error form div.button input").click()
				# time.sleep(1)
				# continue
		# itm = br.find_elements_by_css_selector("div.name a")
		# for it in itm:
			# i = it.get_attribute("href")
			# items.append(i)
			# print i
# cat = br.find_elements_by_css_selector("div#menubar_m1 ul#m1mainSXMenu2 li a.cat")
# catlink = [s.get_attribute("href") for s in br.find_elements_by_css_selector("div#menubar_m1 ul#m1mainSXMenu2 li a.cat")]
# print catlink

# for x in range(len(catlink)):
	# #hover and check if submenu is available
	# hover = ActionChains(br).move_to_element(br.find_elements_by_css_selector("div#menubar_m1 ul#m1mainSXMenu2 li a.cat")[x])
	# print "Mouseover to: " + str(br.find_elements_by_css_selector("div#menubar_m1 ul#m1mainSXMenu2 li a.cat")[x].text)
	# hover.perform()
	# time.sleep(1)
	# if len(br.find_elements_by_css_selector("div.sub-menu-item")) != 0:
		# subcat = br.find_elements_by_css_selector("div.sub-menu-item")
		# print "Submenu found: " + str(len(subcat))
		# print "Iterating each submenu..."
		# for s in range(len(subcat)):
			# #rehover parent item to generate submenu
			# hover = ActionChains(br).move_to_element(br.find_elements_by_css_selector("div#menubar_m1 ul#m1mainSXMenu2 li a.cat")[x])
			# hover.perform()
			# time.sleep(1)
			# #hover current submenu
			# hov = ActionChains(br).move_to_element(br.find_elements_by_css_selector("div.sub-menu-item")[s])
			# hov.perform()
			# time.sleep(1)
			# try:
				# br.find_elements_by_css_selector("div.sub-menu-item")[s].click()
				# time.sleep(1)
				# cat_scrape(br,items)
				# time.sleep(1)
			# except:
				# print "Skipped invisible submenu."
	# else:
		# subcat = br.find_elements_by_css_selector("div.sub-menu-item")
		# print "Submenu found: " +str(len(subcat))
		# #rehover parent item to generate submenu
		# hover = ActionChains(br).move_to_element(br.find_elements_by_css_selector("div#menubar_m1 ul#m1mainSXMenu2 li a.cat")[x])
		# hover.perform()
		# time.sleep(2)
		# print "No submnenu detected. Navigating to "  + str(catlink[x])
		# br.get(catlink[x])
		# time.sleep(1)
		# cat_scrape(br,items)
		# time.sleep(1)

# ulist = list(set(items))
# broken = []
# for i in ulist:
with open("./csv/infile/colorful-garden.csv","rb") as infile:
	for i in infile:
		br.get(i)
		print i
		time.sleep(1)
		tried = 0
		while True:
			try:
				tried = tried + 1
				get_info(br,i,table)
				break
			except:
				if tried < 3:
					br.refresh()
					continue
				else:
					broken.append(i)
					break
			
print "***Job Done***"
              
outfile = open("./csv/outfile/colorful-garden-site-scraped2.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

# errored = open("./csv/outfile/colorful-garden-site-scraped-errored2.csv","wb")
# writer1 = csv.writer(errored)
# writer.writerow(broken)
br.close()