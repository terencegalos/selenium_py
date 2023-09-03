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



url = "https://www.barncandles.com/"
uname = "rick@waresitat.com"
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
	driver.get("https://www.barncandles.com/")
	time.sleep(1)
	try:
		driver.find_element_by_css_selector("#ctl27_dvControl > div > div.navbar-collapse.collapse > div > ul > li:nth-child(3) > a > i").click()
	except:
		driver.find_element_by_css_selector("#ctl28_dvControl > div > div.navbar-collapse.collapse > div > ul > li:nth-child(3) > a").click()
	time.sleep(1)
	driver.find_element_by_id("acctl2816_txtEmailAddress").send_keys(un)
	driver.find_element_by_id("acctl2816_txtPassword").send_keys(pw)
	driver.find_element_by_css_selector("#acctl2816_btnLogin").click()
	time.sleep(1)
	print "Logged in."
	
def get_info(driver,out):

	ls = []
	name = driver.find_element_by_css_selector("#MainForm > div.Layout > section > div > div > section > div.LayoutContentInner > div:nth-child(6) > div.clearfix > div:nth-child(1) > div > div:nth-child(2) > div.page-header.no-m-t > div > h1 > span").text.encode("utf-8")
	sku = driver.find_element_by_css_selector("#lblItemNr")
	cat = "|".join([it.text.encode("utf-8") for it in driver.find_elements_by_css_selector("#lblCategoryTrail > a")])
	vary = driver.find_elements_by_css_selector("select.variantDropDown_30 option")
	variation = []
	try:
		for i in vary:
			variation.append(i.text.encode("utf-8"))
	except:
		variation.append("None")
	min = driver.find_element_by_css_selector("#txtQuantity")
	price = driver.find_element_by_css_selector("#lblPrice")
	image = WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a.main-product-photo.block.zoom.rel")))
	ls.append(name)
	ls.append(sku.text.encode("utf-8"))
	ls.append(cat)
	ls.append(variation)
	ls.append(min.get_attribute("value"))
	ls.append(price.text.encode("utf-8"))
	ls.append(image.get_attribute("href"))
	out.append(ls)
	print ls
	
        
br = init_driver()
init_login(br,uname,passw)
time.sleep(3)
# btn = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ctl37_rpLinkList_ctl00_dvHorizontalNavItem a")))
# btn.click()
# time.sleep(2)



items = []
table = []
links = ["https://www.barncandles.com/store/c/66-Barn-Candles.aspx","https://www.barncandles.com/store/c/31-Barn-Bricks.aspx","https://www.barncandles.com/store/c/32-Barn-Diffusers.aspx","https://www.barncandles.com/store/c/33-Barn-Room-Spray.aspx","https://www.barncandles.com/store/c/28-Accessories.aspx","https://www.barncandles.com/store/c/43-Kitchen-Pantry.aspx","https://www.barncandles.com/store/c/36-Reflective-Light-Inspirations.aspx","https://www.barncandles.com/store/c/41-Reflective-Light-Inspirations-Diffuser.aspx","https://www.barncandles.com/store/c/37-Reflective-Light-Inspirations-Room-Spray.aspx","https://www.barncandles.com/store/c/38-Reflective-Light-Scentiments.aspx","https://www.barncandles.com/store/c/40-Reflective-Light-Scentiments-Room-Spray.aspx",]


with open("./csv/infile/barncandlesku.csv","rb") as infile:
	for i in infile:
		print "Searching for item " + i
		while True:
			try:
				br.find_element_by_css_selector("div > div.navbar-collapse.collapse > div > ul > li:nth-child(1) > a > i").click()
				time.sleep(.5)
				br.find_element_by_id("txtRedirectSearchBox").clear()
				br.find_element_by_id("txtRedirectSearchBox").send_keys(i)
				br.find_element_by_id("btnSearchBox").click
				time.sleep(1)
				break
			except:
				br.refresh()
				time.sleep(1)
				continue
		try:
			item = br.find_element_by_css_selector("#MainForm > div.Layout > section > div > div > section > div.LayoutContentInner > div.product-list > div > div > div > div > div.no-m-b > a").get_attribute("href")
			print "Item found " + str(item)
			items.append(item)
		except:
			try:
				get_info(br,table)
			except:
				print "Item not found."
		
		

    


for i in items:
	print "Navigating to:\n" + str(i)
	br.get(i)
	time.sleep(1)
	get_info(br,table)


print "***Job Done***"        
        
outfile = open("./csv/outfile/barncandles.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)