

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
        pasw = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#enterPasswordDialoginputWithValidation3input")))
        pasw.send_keys(pw)
        driver.find_element_by_css_selector("#enterPasswordDialogsubmitButton").click()
        time.sleep(5)
        print "Logged in."
    except:
        print "Log in failed."         
        
        
def get_info(driver,link,out):

    driver.get(link)
    time.sleep(1)
    name = driver.find_element_by_id("item-contenttitle")
    sku = driver.find_element_by_css_selector("div.code em")
    cat = driver.find_element_by_css_selector("div.breadcrumbs")
    desc = driver.find_element_by_id("caption")
    
    try:
        vary = driver.find_elements_by_tag_name("option")
    except:
        vary = "none"
    
    try:
        image = driver.find_element_by_css_selector("img.image-l")
    except:
        image = "none"
    
    try:
        for i in vary:
            ls = []
            ls.append(name.text.encode("utf-8"))
            ls.append(i.text.encode("utf-8"))
            ls.append(sku.text.encode("utf-8"))
            ls.append(cat.text.encode("utf-8"))
            ls.append(desc.text.encode("utf-8"))
            try:
                ls.append(image.get_attribute("src"))
            except:
                ls.append(image)
            print ls
            out.append(ls)
    except:
        ls = []
        ls.append(name.text.encode("utf-8"))
        ls.append(vary)
        ls.append(sku.text.encode("utf-8"))
        ls.append(cat.text.encode("utf-8"))
        ls.append(desc.text.encode("utf-8"))
        try:
            ls.append(image.get_attribute("src"))
        except:
            ls.append(image)
        print ls
        out.append(ls)        
        

        
###################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
links = ["http://www.seventhmusewholesale.com/#!medallion-rings/cw6m","http://www.seventhmusewholesale.com/#!cameo-rings/c1stu","http://www.seventhmusewholesale.com/#!medallion-rings/cw6m","http://www.seventhmusewholesale.com/#!birthstone/c19bg","http://www.seventhmusewholesale.com/#!cameo-earrings/c1lep","http://www.seventhmusewholesale.com/#!tear-drop-earrings/c1ln8","http://www.seventhmusewholesale.com/#!card-necks/c46w","http://www.seventhmusewholesale.com/#!mala-necklaces/c1qb5","http://www.seventhmusewholesale.com/#!jewelry/cjg9","http://www.seventhmusewholesale.com/#!perfume-oils/cee5","http://www.seventhmusewholesale.com/#!mists/c1qs2"]        
ln = "http://www.seventhmusewholesale.com/#!medallion-rings/cw6m"   

category = []
items = []

br = init_driver()
time.sleep(1)

cats = br.find_element_by_css_selector("#menubar1 li.sf_first_nav_item a")
for cat in cats:
	lnk = cat.get_attribute("href")
	print lnk
	category.append(lnk)

	
for ct in category:
	br.get(ct)
	time.sleep(1)
	item = br.find_elements_by_css_selector("body div.sf_outer_wrapper div.sf_wrapper div.sf_main_wrapper div div div div.main-content div div.products.clearfix table tbody tr td a")
	for itm in item:
		it = itm.get_attribute("href")
		print it
		items.append(it)
		

for i in items:
	ls = []
	br.get(i)
	time.sleep(1)
	name = br.find_element_by_css_selector("body div.sf_outer_wrapper div.sf_wrapper div.sf_main_wrapper div div div div.main-content div div.product-detail.content-block div.product-secondary div.product-detail-header h1").text.encode("utf-8")
	desc = br.find_element_by_css_selector("body div.sf_outer_wrapper div.sf_wrapper div.sf_main_wrapper div div div div.main-content div div.product-detail.content-block div.product-primary div.product-description").text.encode("utf-8")
	cat = br.find_element_by_css_selector("#breadcrumbs").text.encode("utf-8")
	minqty = br.find_element_by_css_selector("#addToCartForm div div.quantity span.field input[type=\"text\"]").get_attribute("value")
	price = br.find_element_by_css_selector("#listPrice").text.encode("utf-8")
	image = br.find_element_by_css_selector("#filmstripPreview").get_attribute("src")
	option = []
	try:
		option = br.find_element_by_css_selector("select option")
		for opt in option:
			op = opt.text.encode("utf-8")
			print op
			options.append(op)
	except:
		print "Options not available for this item."
		option = "No options."
		
	ls.append(name)
	ls.append(desc)
	ls.append(cat)
	ls.append(minqty)
	ls.append(price)
	ls.append(image)
	ls.append(option)
    


             
        
outfile = open("./csv/outfile/seventhmuse_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(items)

print "***Job Done***"        
   