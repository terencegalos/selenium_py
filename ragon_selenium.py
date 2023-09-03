from selenium import webdriver
import time
import urllib
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains
from urllib2 import urlopen
import csv

page = "https://ragonhouse.com/everyday-en-3/christmas1/?sef_rewrite=1&utm_source=Copy+of+Online+Warehouse+Sale+2014&utm_campaign=Ragon+House+ONLINE+WAREHOUSE+CLEARANCE+SALE&utm_medium=email&items_per_page=128"
uname = "rick@waresitat.com"
pw = "wolfville"
url = "http://ragonhouse.com/"
sale = "http://ragonhouse.com/sale/"
def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]
    
def init_login(driver,un,passw):
	driver.get(url)
	ActionChains(driver).move_to_element(driver.find_element_by_css_selector("#sw_dropdown_778 > a")).perform()
	time.sleep(1)
	driver.find_element_by_css_selector("#sw_dropdown_778 > a").click()
	time.sleep(1)
	driver.find_element_by_css_selector("#account_info_778 > div.ty-account-info__buttons.buttons-container > a.ty-btn.ty-btn__primary").click()
	time.sleep(1)
	try:
		print "Logging in..."
		WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "login_main_login"))).send_keys(un)
		WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "psw_main_login"))).send_keys(pw)
		time.sleep(8)
		btn = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.NAME, "dispatch[auth.login]")))
		btn.click()
		print ("Login Success.")
	except:
		print "Login failed."
		br.close()
		
def get_info(driver,table):
	ls = []
	time.sleep(2)
	name = driver.find_element_by_css_selector("h1.ty-product-block-title").text.encode("utf-8")
	sku = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ty-control-group__item")))
	cat = "|".join([i.text.encode("utf-8") for i in driver.find_elements_by_css_selector("a.ty-breadcrumbs__a")])
	desc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ty-product-block__price-actual")))
	minimum = driver.find_element_by_css_selector("p.description").text.encode("utf-8")
	mins = driver.find_elements_by_css_selector("div.ty-qty-discount > table > thead > tr > th")
	hover = ActionChains(driver).move_to_element(br.find_element_by_css_selector("div.ty-product-block__img-wrapper"))
	hover.perform()
	time.sleep(2)
	image = driver.find_element_by_css_selector("body div.cloudzoom-zoom img").get_attribute("src")
	
	ls.append(name)
	ls.append(sku.text.encode("utf-8"))
	ls.append(desc.text.encode("utf-8"))
	ls.append(cat)
	ls.append(minimum)
	ls.append(image)
	for x in range(1,len(mins)):
		min = driver.find_elements_by_css_selector("div.ty-qty-discount > table > thead > tr > th")[x].text.encode("utf-8")
		price = driver.find_elements_by_css_selector("div.ty-qty-discount > table > tbody > tr > td")[x].text.encode("utf-8")
		ls.append(min)
		ls.append(price)
	table.append(ls)
	print ls
        
#initialize and open browser
br = init_driver()
time.sleep(1)
init_login(br,uname,pw)

items = []
time.sleep(8)
table = []
with open("./csv/infile/ragon_sku.csv","rb") as infile:
    for i in infile:
        print "Searching for item " + str(i)
        while True:
            try:
                try:
                    br.find_element_by_name("q").clear()
                except:
                    br.find_element_by_name("hint_q").clear()
                try:
                    br.find_element_by_name("q").send_keys(i)
                except:
                    br.find_element_by_name("hint_q").send_keys(i)
                break
            except:
                br.refresh()
                continue
            
        time.sleep(1)
        try:
			ls = []
            # print "Getting all items in this page..."
            # item = br.find_elements_by_css_selector("a.product-title")
            # for it in item:
                # items.append(it.get_attribute("href"))
                # print it.get_attribute("hrefk
			sku = br.find_element_by_css_selector("#pagination_contents > div.grid-list > div > div > form > div.ty-grid-list__item-name > div").text.split()[1]
			image = br.find_element_by_css_selector("img.ty-pict").get_attribute("src")
			ls.append(sku)
			ls.append(image)
			print ls
			table.append(ls)
        except:
            print "Item not found."
# br.get(sale)
# time.sleep(1)
# ActionChains(br).move_to_element(br.find_element_by_css_selector("#sw_elm_pagination_steps")).perform()
# time.sleep(1)
# br.find_element_by_css_selector("#sw_elm_pagination_steps").click()
# time.sleep(1)
# br.find_element_by_css_selector("#elm_pagination_steps li:nth-child(4) a").click()
# time.sleep(1)
# item = [itm.get_attribute("href") for itm in br.find_elements_by_css_selector("a.product-title")]
# for i in item:
	# items.append(i)
	# print i
	
# br.find_element_by_css_selector("#pagination_contents div.ty-pagination__bottom div a.ty-pagination__item.ty-pagination__btn.ty-pagination__next.cm-history.cm-ajax").click()
# time.sleep(10)
# item = [itm.get_attribute("href") for itm in br.find_elements_by_css_selector("a.product-title")]
# for i in item:
	# items.append(i)
	# print i

# for item in list(set(items)):
	# while True:
		# try:
			# br.get(item)
			# time.sleep(1)
			# get_info(br,table)
			# break
		# except:
			# br.refresh()
			# time.sleep(1)
			# continue
    

outfile = open('./csv/outfile/ragon_output.csv','wb')
writer = csv.writer(outfile)
writer.writerows(table)