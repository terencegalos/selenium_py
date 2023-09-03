from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv

uname = "rstuart"
pw = "Wolfville4"
URL = "https://www.carsonhomeaccents.com/security_logon.asp?autopage=%2Fdefault%2Easp"
items = []

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):    
    driver.get(URL)
    try:
        print "Logging in..."
        driver.find_element_by_id('logonUsername').send_keys(un)
        driver.find_element_by_id('logonPassword').send_keys(pw)
        driver.find_element_by_name('B1').click()

        print ("Login Success.")
    except:
        print "Login failed."
		
def get_info(driver,item,out):
	ls = []
	print "Navigating to item: " + str(item)
	driver.get(item)
	try:
		option = driver.find_elements_by_css_selector("select#prod_opt1 option")
		print "Option detected..."
		time.sleep(1)
		name = driver.find_element_by_id("detail_parent_prod_nm").text.encode("utf-8")
		desc = driver.find_element_by_class_name("detail_desc_content").text.encode("utf-8")
		image = driver.find_element_by_id("detail_enlarge").get_attribute("href")
		
		try:
			sku = driver.find_element_by_css_selector("#sku_container").text.encode("utf-8")
		except:
			sku = driver.find_element_by_css_selector("#detail_info_sku > span:nth-child(2)").text.encode("utf-8")
		ls.append(sku)
		ls.append(desc)
		ls.append(image)
		ls.append(driver.find_elements_by_css_selector("select#prod_opt1 option")[0].text.encode("utf-8"))
		out.append(ls)
		print ls
		# get the rest of option
		for opt in range(1,len(option)):
			driver.find_elements_by_css_selector("select#prod_opt1 option")[opt].click()
			print "Option selected."
			time.sleep(1)
			
			try:
				sku = driver.find_element_by_css_selector("#sku_container").text.encode("utf-8")
			except:
				sku = driver.find_element_by_css_selector("#detail_info_sku > span:nth-child(2)").text.encode("utf-8")
			ls.append(name)
			ls.append(sku)
			ls.append(desc)
			ls.append(image)
			ls.append(driver.find_elements_by_css_selector("select#prod_opt1 option")[opt].text.encode("utf-8"))
			out.append(ls)
			print ls
	except:
		name = driver.find_element_by_css_selector("#detail_parent_prod_nm").text.encode("utf-8")
		try:
			sku = driver.find_element_by_css_selector("#sku_container").text.encode("utf-8")
		except:
			sku = driver.find_element_by_css_selector("#detail_info_sku > span:nth-child(2)").text.encode("utf-8")
		desc = driver.find_element_by_class_name("detail_desc_content").text.encode("utf-8")
		image = driver.find_element_by_id("detail_enlarge").get_attribute("href")
		ls.append(name)
		ls.append(sku)
		ls.append(desc)
		ls.append(image)
		out.append(ls)
		print ls
	print "**Attributes scraped."

#initialize and open browser
br = init_driver()
init_login(br,uname,pw)

items = []
table = []
# with open('./csv/infile/carsonsku.csv','rb') as infile:
    # for i in infile:
		# while True:
			# try:
				# br.find_element_by_id("search_keyword").clear()
				# br.find_element_by_id("search_keyword").send_keys(i)
				# time.sleep(1)
				# break
			# except:
				# time.sleep(1)
				# br.refresh()
				# continue
		# try:
			# it = [i.get_attribute("href") for i in br.find_elements_by_css_selector("div.item_row.nm a")]
			# items.extend(it)
			# print it
			# print "Saved..."
		# except:
			# print "Item not found."

        
# print "**All items saved.***"
# outfile1 = open('./csv/outfile/carson_items.csv','wb')
# writer1 = csv.writer(outfile1)
# writer1.writerow(items)

# table = []
# for i in set(items):
	# while True:
		# try:
			# get_info(br,i,table)
			# break
		# except:
			# br.refresh()
			# time.sleep(1)
			# continue
cats = [cat.get_attribute("href") for cat in br.find_elements_by_css_selector("#megamenu1 > div > h3 > a")]
for cat in cats:
	print "Category visit: " + cat
	br.get(cat)
	time.sleep(2)
	#get total no of checkbox
	checkbox = br.find_elements_by_css_selector("label > input[type=\"checkbox\"]")
	#go each check box for items
	for x in range(len(checkbox)):
		#expand category to make checkbox visible
		expander = br.find_elements_by_css_selector("div.nys_subtitle.ui-dialog-titlebar.ui-widget-header.ui-corner-all")
		for r in expander:
			r.click()
			time.sleep(1)
		time.sleep(1)
		br.find_elements_by_css_selector("label > input[type=\"checkbox\"]")[x].click()
		cat = br.find_element_by_css_selector("#nys_window > div.nys_selections > div.nys_selected.ui-corner-all").text.encode("utf-8")
		time.sleep(1)
		print "Loading all items..."
		#view 120 items/page
		br.find_element_by_css_selector("#rpp1 > option:nth-child(5)").click()
		time.sleep(1)
		#store sku in an array
		skus = br.find_elements_by_css_selector("div.item_row.sku.sku_original")
		for sku in skus:
			ls = []
			ls.append(sku.text.split()[1])
			ls.append(cat)
			print ls
			table.append(ls)
		#pagination if available
		while True:
			try:
				br.find_element_by_link_text("next").click()
				time.sleep(1)
				print "...next page"
				skus = br.find_elements_by_css_selector("div.item_row.sku.sku_original")
				for sku in skus:
					ls = []
					ls.append(sku.text.split()[1])
					ls.append(cat)
					print ls
					table.append(ls)
			except:
				print "Pagination exhausted."
				break
		#remove filter then proceed to next cat
		print "Removing filter..."
		br.find_element_by_link_text("x").click()
		time.sleep(1)
		
	
outfile = open('./csv/outfile/carson_cat_results.csv','wb')
writer = csv.writer(outfile)
writer.writerows(table)

print "Job done."