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
	# driver.find_element_by_css_selector("#header ul li:nth-child(1) a").click()
	driver.find_element_by_css_selector("#header-account > ul > li.last > a").click()
	time.sleep(1)
	driver.find_element_by_name("login[username]").send_keys(un)
	driver.find_element_by_name("login[password]").send_keys(pw)
	driver.find_element_by_name("send").click()
	time.sleep(5)
	print "Logged in."

def get_benson(driver,link,out):
	driver.get(link)
	time.sleep(1)
	name = driver.find_element_by_css_selector("#product_addtocart_form div.product-shop div.product-name h1").text.encode("utf-8")
	desc = driver.find_element_by_css_selector("#product_addtocart_form div.product-shop div.short-description div.std").text.encode("utf-8")
	regprice = "Regprice displayed 0" if driver.find_element_by_css_selector("div.price-box span.regular-price span.price").text.encode("utf-8") == "0" else driver.find_element_by_css_selector("div.price-box span.regular-price span.price").text.encode("utf-8")
	pic = driver.find_element_by_css_selector("#image-zoom").get_attribute("href")
	tierprice = []
	try:
		tier = driver.find_elements_by_css_selector("#product_addtocart_form div.product-shop ul li")
		tierprice.append([t.text.encode("utf-8") for t in [tier]])
	except:
		print "No tier pricing found."
		tierprice.append("No tier pricing.")
	info = driver.find_elements_by_css_selector("#product-options-wrapper div dl")
	ls = []
	options = []
    #loop each option and check for available tags
	for inf in info:
		option = []
		option.append(inf.find_element_by_tag_name("dt").text.encode("utf-8"))
		print inf.get_attribute("innerHTML")
		try:
			for o in inf.find_elements_by_css_selector("dd select option"):
				option.append(o.text)
		except:
			print "No select tags..."
		try:
			for c in inf.find_elements_by_css_selector("ul.options-list li"):
				option.append(c.text)
				print c.text
			print "Checkboxes found..."
		except:
			print "Check boxes not found."
		try:
			inf.find_element_by_css_selector("dd input.input-text")
			print "Input text found..."
			option.append("input text")
			try:
				option.append(inf.find_element_by_css_selector("dd a img").get_attribute("src"))
			except:
				option.append("No image for text option.")
			print option
		except:
			print "Unknown option found. Investigate and fix..."
		options.append(option)
		
	ls.append(name)
	ls.append(desc)
	ls.append(regprice)
	ls.append(tierprice)
	ls.append(options)
	ls.append(pic)
	out.append(ls)
	print ls

test = "http://bensonmarketinggroup.com/country-primitive/bags/cotton-jute-bags/linen-wine-bags.html"
test1 = "http://bensonmarketinggroup.com/custom-packaging/string-tags/custom-earring-cards-233.html"
test2 = "http://bensonmarketinggroup.com/bags/reusable-bags/zipper-shoulder-tote.html"
test3 = "http://bensonmarketinggroup.com/country-primitive/business-cards/custom-kraft-business-cards.html"
test4 = "http://bensonmarketinggroup.com/bags/packaging-collections/animal-paper-shoppers.html"

		
br = init_driver()
init_login(br,uname,passw)
time.sleep(1)

items = []
table = []
cats = []
morecats = []

cat = br.find_elements_by_css_selector("#navigation ul li ul li a")
print "Navigating each top level links..."
for ct in cat:
	c = ct.get_attribute("href")
	cats.append(c)
	print "Found - " + str(c)
	time.sleep(1)

for c in cats:
	print "Navigating to " + str(c)
	br.get(c)
	time.sleep(1)
	try:
		item = br.find_elements_by_css_selector("#container div div.category-products div ul.products-grid div div div h5.product-name a")
		print "Items found. Saving links..."
		for i in item:
			itm = i.get_attribute("href")
			items.append(itm)
			print itm
	except:
		morecat = br.find_elements_by_css_selector("#container div div.boxes div div div h5 a")
		print "Found more categories."
		for more in morecat:
			morcat = more.get_attribute("href")
			print morcat
			morecats.append(morcat)
		
for mc in morecats:
	print "Navigating to " + str(mc)
	br.get(mc)
	time.sleep(1)
	try:
		item = br.find_elements_by_css_selector("#container div div.category-products div ul.products-grid div div div h5.product-name a")
		for i in item:
			itm = i.get_attribute("href")
			print itm
			items.append(itm)
	except:
		morecat = br.find_elements_by_css_selector("#container div div.boxes div div div h5 a")
		for more in morecat:
			morcat = more.get_attribute("href")
			print morcat
			items.append(morcat)
			
ulist = list(set(items))	
		
		
outfile = open("./csv/outfile/bensonmarketinggroup_items.csv","wb")
writer = csv.writer(outfile)
writer.writerow(ulist) 