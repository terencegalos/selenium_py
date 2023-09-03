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



login = "http://desma-group.com/customer/account/login/"
url = "http://www.seventhmusewholesale.com/"
uname = "rick@waresitat.com"
passw = "seventhmuse"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
    
def init_login(driver,un,pw):
	print "Navigating to " + str(url) + " and logging in..."
	driver.get(url)
	print "Logging in."
	try:
		WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#enterPasswordDialoginputWithValidation1input"))).send_keys(pw)
		driver.find_element_by_css_selector("#enterPasswordDialogsubmitButton").click()
		time.sleep(5)
		print "Logged in."
	except:
		print "Success."
		driver.close()
        
        
def get_items(driver,out):
	#get items the first time
	it = [i.get_attribute("href") for i in driver.find_elements_by_css_selector("#frmCompare ul li div.ProductDetails strong a")]
	for i in list(set(it)):
		out.append(i)
		print i
	#click next page until exhausted
	while True:
		try:
			driver.find_element_by_css_selector("#CategoryPagingBottom div div.FloatRight a").click()
			time.sleep(1)
			print "Next page clicked.."
			it = [i.get_attribute("href") for i in driver.find_elements_by_css_selector("#frmCompare ul li div.ProductDetails strong a")]
			for i in list(set(it)):
				out.append(i)
				print i
		except:
			print "Next page exhausted."
			time.sleep(1)
			break

def get_info(driver,link,out):
	driver.get(link)
	time.sleep(1)
	name = driver.find_element_by_css_selector("#ProductDetails div div.ProductMain h1").text.encode("utf-8")
	sku = driver.find_element_by_css_selector("span.VariationProductSKU").text.encode("utf-8")
	cat = driver.find_elements_by_css_selector("#ProductBreadcrumb ul li")
	desc = driver.find_element_by_css_selector("#ProductDescription div").text.encode("utf-8")
	regprice = driver.find_element_by_css_selector("#ProductDetails div div.ProductMain div.ProductDetailsGrid div.ProductPriceWrap div.DetailRow.PriceRow div em").text.encode("utf-8")
	slide = driver.find_elements_by_css_selector("#ProductDetails div div.ProductAside div.ImageCarouselBox div ul li div div a img")
	images = []
	for s in range(len(slide)):
		ActionChains(driver).move_to_element(driver.find_elements_by_css_selector("#ProductDetails div div.ProductAside div.ImageCarouselBox div ul li div div a img")[s]).perform()
		time.sleep(1)
		while True:
			try:
				images.append(driver.find_element_by_css_selector("div.zoomPad img").get_attribute("src"))
				break
			except:
				driver.refresh()
				time.sleep(1)
				continue
	try:
		text = []
		detail = driver.find_elements_by_css_selector("#productDetailsAddToCartForm div div.DetailRow")
		for d in detail:
			text.append(d.find_element_by_css_selector("div.Label").text.encode("utf-8"))
			text.append(d.find_element_by_css_selector("div.Value").text.encode("utf-8"))
	except:
		text = "No text input."
		print "No text input."
		
	info = driver.find_elements_by_css_selector("div.productAttributeRow")
	options = []
    #loop each option and check for available tags
	for inf in info:
		option = []
		option.append(inf.find_element_by_css_selector("div.productAttributeLabel").text.encode("utf-8"))
		try:
			for o in inf.find_elements_by_css_selector("div.productAttributeValue label span"):
				option.append(o.text.encode("utf-8"))
		except:
			print "No checkboxes found..."
		try:
			for c in inf.find_elements_by_css_selector("div.productAttributeValue div.productOptionViewSelect select option"):
				if "--" in c.text:
					print "Skipped."
					time.sleep(1)
				else:
					option.append(c.text.encode("utf-8"))
					print c.text
			print "Select tag found..."
		except:
			print "Select tag not found."
		options.append("|".join(map(str,option)))
		
	ls = []
	ls.append(name)
	ls.append(sku)
	ls.append("|".join(map(str,[c.text for c in cat])))
	ls.append(desc)
	ls.append(regprice)
	ls.append("|".join(map(str,images)))
	ls.append("||".join(map(str,options)))
	ls.append(text)
	out.append(ls)
	print "\n"
	print [s for s in ls]
	print "\n"
        
###################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

br = init_driver()
time.sleep(1)
br.get("http://www.gellitecandles.com/")
time.sleep(3)

table = []
# #get categories
# cat = [s.get_attribute("href") for s in br.find_elements_by_css_selector("#SideCategoryList div ul.category-list li a")]
# items = []
# table = []

# #iterate each get and subcategory or items
# for c in range(len(cat)):
	# print "Navigating to " + cat[c]
	# #check subcategory found
	# if c == 0 or c == 2:
		# br.get(cat[c])
		# time.sleep(1)
		# cats = [ct.get_attribute("href") for ct in br.find_elements_by_css_selector("#CategoryHeading div div.SubCategoryListGrid ul li a")]
		# print "Subcategory found. Navigating each"
		# for item in cats:
			# print "Navigating subcategory " + item
			# br.get(item)
			# time.sleep(1)
			# get_items(br,items)
	# #if no subcategory
	# else:
		# print "No subcategory. Getting items immediately..."
		# get_items(br,items)

# ulist = list(set(items))

# outfile1 = open("./csv/outfile/gellitecandles_items.csv","wb")
# writer = csv.writer(outfile1)
# writer.writerow(ulist)


with open("./csv/infile/gellitecandles_items.csv","rb") as infile:
	for item in infile:
		while True:
			try:
				get_info(br,item,table)
				break
			except:
				br.refresh()
				time.sleep(3)
				continue
				
outfile = open("./csv/outfile/gellitecandles_results1.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"
br.close()