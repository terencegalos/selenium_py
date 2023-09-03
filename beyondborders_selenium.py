from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv


URL = "http://www.beyondbordersfairtrade.com/"
uname = "rick@waresitat.com"
pwd = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def is_text_present (brw, string):
    brw.switch_to_default_content()
    if str(string) in brw.page_source:
        return True
    else:
        return False
    
def init_login(driver,un,pw):    
    driver.get(URL)
    time.sleep(1)
    driver.find_element_by_css_selector("#home > div.page > div.header > div > div.TopMenu > div > ul > li:nth-child(3) > a").click()
    time.sleep(1)
    
    print "Logging in..."
    driver.find_element_by_css_selector('#id_username').send_keys(un)
    driver.find_element_by_css_selector('#id_password').send_keys(pw)
    driver.find_element_by_css_selector('body > div > div > div > div:nth-child(2) > div > form > div > input').click()

    print "Success."
    time.sleep(1)

def get_info(driver,out):
	ls = []
	# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#direct-catalog > div.container > div > div.catalog-view.content > div > div.results.search > ul > li.span4.quote-line-image > div > a.square-image-wrapper.show-details-modal")))
	# driver.find_element_by_css_selector("#direct-catalog > div.container > div > div.catalog-view.content > div > div.results.search > ul > li.span4.quote-line-image > div > a.square-image-wrapper.show-details-modal").click()
	# time.sleep(1)
	
	title = driver.find_element_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-details > h3").text.encode("utf-8")
	sku = driver.find_element_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-details > p.price-and-sku > span.sku").text.encode("utf-8")
	cat = "|".join([i.text.encode("utf-8") for i in driver.find_elements_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-details > div.breadcrumbs a")])
	desc = driver.find_element_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-details > p.pre").text.encode("utf-8")
	price = driver.find_element_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-details > p.price-and-sku > span.unit-price > span").text.encode("utf-8")
	image = driver.find_element_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-images > div > a > div.square-wrapper > img").get_attribute("src")    
	ls.append(title)
	ls.append(sku.split()[1])
	ls.append(cat)
	ls.append(desc)
	ls.append(price)
	ls.append(image)
	print ls
	out.append(ls)
	driver.find_element_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-header > a").click()
    
    
        
br = init_driver()
init_login(br,uname,pwd)
        
        
        
table = []        
with open("./csv/infile/bborders.csv","rb") as infile:
	for i in infile:
		while True:
			try:
				br.find_element_by_css_selector("#buyer-nav-search > input").clear()
				br.find_element_by_css_selector("#buyer-nav-search > input").send_keys(i.strip())
				br.find_element_by_css_selector("#buyer-nav-search > input").send_keys(Keys.ENTER)
				time.sleep(1)
				break
			except:
				br.refresh()
				time.sleep(1)
				continue
		try:
			br.find_element_by_css_selector("#taxonomy_catalog > div > div.results > ul > li.span4.quote-line-image > div > a.square-image-wrapper.show-details-modal").click()
			print i.strip()
			time.sleep(1)
			get_info(br,table)
		except:
			print "No item found."
		
print "**Items scraped**"


    
outfile = open("./csv/outfile/bborders_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"
br.close()