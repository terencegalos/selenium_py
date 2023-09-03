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



login = "http://www.americaretold.com/index.php/retailer-access.html"
url = "http://www.americaretold.com/"
uname = "holly"
passw = "baragry"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
    
def init_login(driver,un,pw):
	print "Navigating to " + str(url) + " and logging in..."
	driver.get(login)
	print "Logging in."
	try:
		WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME,"username"))).send_keys(un)
		WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME,"password"))).send_keys(pw)
		WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME,"Submit"))).click()
		time.sleep(2)
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
init_login(br,uname,passw)
time.sleep(4)

table = []
items = []
# section = ["Closeouts at -50%","Signs"]
# for sect in section:
	# br.find_element_by_link_text(sect).click()
	# time.sleep(1)
	# cat = [itm.get_attribute("href") for itm in br.find_elements_by_css_selector("#menu ul li.active.deeper.parent ul li ul li.active.deeper.parent ul li a")]
	# for i in cat:
		# print "Navigating to " + str(cat)
		# br.get(i)
		# time.sleep(1)
		# ActionChains(br).move_to_element(br.find_element_by_css_selector("select.chzn-done.inputbox")).perform()
		# time.sleep(1)
		# br.find_element_by_css_selector("select.chzn-done.inputbox option:nth-child(6)").click()
		# time.sleep(3)
		# item = br.find_elements_by_css_selector("span.hikashop_product_name a")
		# try:
			# ct = br.find_element_by_css_selector("div.hikashop_category_information.hikashop_products_listing_main h1").text.encode("utf-8")
		# except:
			# ct = (br.current_url.split("/")[-1]).split(".")[0]
		# for it in item:
			# pair = []
			# pair.append(it.get_attribute("href"))
			# pair.append(ct)
			# print pair
			# items.append(pair)
	
# outfile1 = open("./csv/infile/america_retold_items.csv","wb")
# writer1 = csv.writer(outfile1)
# writer1.writerow(items)


with open("./csv/infile/america_retold_items.csv","rb") as infile:
	for prod in infile:
		print prod
		print "Getting info for item " + str(prod.split(",")[0])
		br.get(prod.split(",")[0].strip("\""))
		time.sleep(1.5)
		while True:
			try:
				sku = br.find_element_by_css_selector("span.hikashop_product_code_main").text.strip()
				break
			except:
				print "Sku not detected. Retrying..."
				br.refresh()
				time.sleep(2)
				continue
        while True:
            try:
                name = br.find_element_by_id("hikashop_product_name_main").text.strip()
                break
            except:
                print "No name detected. Retrying..."
                br.refresh()
                time.sleep(2)
                continue
		desc = br.find_element_by_id("hikashop_product_description_main").text.strip()
        while True:
            try:
                price = br.find_element_by_css_selector("span.hikashop_product_price_full").text.strip()
                break
            except:
                print "Price not detected. Retrying..."
                br.refresh()
                time.sleep(2)
                continue
        while True:
            try:
                minqty = br.find_element_by_css_selector("input.hikashop_product_quantity_field").get_attribute("value")
                break
            except:
                print "Minimum not detected. Retrying..."
                br.refresh()
                time.sleep(2)
                continue
        while True:
            try:
                dim = br.find_element_by_css_selector("span.hikashop_product_width_main").text.encode("utf-8") + " x " + br.find_element_by_css_selector("span.hikashop_product_height_main").text.encode("utf-8")
                break
            except:
                print "Dimension not detected. Retrying..."
                br.refresh()
                time.sleep(2)
                continue
		ActionChains(br).move_to_element(br.find_element_by_id("hikashop_main_image")).perform()
		time.sleep(1)
		image = br.find_element_by_css_selector("#hikashop_main_image_link").get_attribute("href")
		
		ls = []
		
		ls.append(name)
		ls.append(sku)
		ls.append(prod.split(",")[1])
		ls.append(desc)
		ls.append(dim)
		ls.append(minqty)
		ls.append(price)
		ls.append(image)
		
		print ls
		table.append(ls)
				
outfile = open("./csv/outfile/america_retold.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"
br.close()