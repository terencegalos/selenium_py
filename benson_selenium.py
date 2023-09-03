from selenium import webdriver
import time
import urllib
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


url = "http://bensonmarketinggroup.com/"
uname = "rick@waresitat.com"
passw = "wolfville"


def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser
    
def init_login(driver,un,pw):
	driver.get(url)
	time.sleep(1)
	#driver.find_element_by_css_selector("#header ul li:nth-child(1) a").click()
	driver.find_element_by_css_selector("#header-account > ul > li.last > a").click()
	time.sleep(1)
	driver.find_element_by_name("login[username]").send_keys(un)
	driver.find_element_by_name("login[password]").send_keys(pw)
	driver.find_element_by_name("send").click()
	time.sleep(5)
	print "Logged in."
	
def item_splitter(arr,ls,flag = 0):
	if(flag):		
		for x in l:
			arr.append(ls)			
	else:
		arr.append(ls)

def get_benson(driver,link,out):
	ls = []
	driver.get(link)
	time.sleep(1)
	cat = "|".join([c.text for c in driver.find_elements_by_css_selector("div.breadcrumbs ul li")])
	name = driver.find_element_by_css_selector("#page-columns > div > div.product-view.nested-container > div.product-primary-column.product-shop.grid12-5 > div.product-name > h1").text.encode("utf-8")
	desc = driver.find_element_by_css_selector("#page-columns > div > div.product-view.nested-container > div.product-primary-column.product-shop.grid12-5 > div.short-description > div").text.encode("utf-8")
	pic = driver.find_element_by_css_selector("#zoom1").get_attribute("href")
	option = br.find_elements_by_css_selector("#product-options-wrapper > div > dl") # detecting multiple options
	optlist = []
	for count,opt in enumerate(option):
		curr = ""
		flag = 0
		try:
			label = opt.find_element_by_css_selector("dt").text.encode("utf-8")
		except:
			label = "No label"
		optext = opt.get_attribute("innerHTML")
		#print optext
		if "type=text" in optext: # textarea tag
			curr = "text input"
		elif "textarea" in optext: #textarea tag
			curr = "textarea"
		elif "type=file" in optext: #input type=file tag
			curr = "file upload"
		elif "radio-checkbox-text" in optext: #radio button tag
			curr = opt.find_elements_by_css_selector("dd div.radio-checkbox-text")
			curr = "|".join([i.text for i in curr])
			if "$" in curr:
				flag = 1
		elif "img" in optext:
			curr =  opt.find_element_by_css_selector("dd a").get_attribute("href")
		elif "<option" in optext: #option tag
			curr = opt.find_elements_by_css_selector("dd select option")
			curr = "|".join([i.text for i in curr])
		elif "<ul" in optext: # list tag
			curr = opt.find_elements_by_css_selector("dd ul li")
			curr = "|".join([i.text for i in curr])
			if "$" in curr:
				flag = 1
		else:
			print "Some error occurred. Check again."
			print opt.find_element_by_css_selector("dd").get_attribute("innerHTML")
			time.sleep(5)
		print label
		print curr
		curr = "|".join([label,curr])
		item_splitter(optlist,curr,flag)
	
	ls.append(name)
	ls.append(cat)
	ls.append(desc)
	ls.append(pic)
	for lst in optlist:
		ls.append(lst)	
	print ls
	table.append(ls)
		
br = init_driver()
init_login(br,uname,passw)
time.sleep(1)

items = []
table = []

# with open("./csv/infile/bensonmarketinggroup_items.csv","rb") as infile:
	# for item in infile:
		# get_benson(br,item,table)
		
cats = [it.get_attribute("href") for it in br.find_elements_by_css_selector("#mainmenu > ul > li > div > div > div > ul > li > a")]
#cats = [it.get_attribute("href") for it in br.find_elements_by_css_selector("#mainmenu > ul > li > div > div > div > ul > li > a")]
for cat in cats[2:3]:
	print cat
	br.get(cat)
	time.sleep(1)
	item = [lnk.get_attribute("href") for lnk in br.find_elements_by_css_selector("#page-columns > div.column-main > div.category-products > ul > li > h2 > a")]
	for t in item:
		print t
		items.append(t)
		
# for item in set(items):
	# print item
	# get_benson(br,item,table)
	
for x in range(len(items)):
	print "\nOpening link "+items[x]+"\n"
	get_benson(br,items[x],table)
	
outfile = open("./csv/outfile/bensonmarketinggroup_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)