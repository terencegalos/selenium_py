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
from selenium.webdriver.common.keys import Keys

url = "http://vhcbrands.com/"
home = "http://vhcbrands.com/Brand/Home"
bella = "http://vhcbrands.com/Brand/BellaTaylor/Lifestyle/Bella-Taylor"
login = "http://bethanylowe.com/login"
uname = "rick@waresitat.com"
passw = "wolfville"


def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    driver.get(url)
    time.sleep(3)
    br.find_element_by_css_selector("#sw_dropdown_778 a").click()
    time.sleep(3)
    br.find_element_by_css_selector("#account_info_778 div.ty-account-info__buttons.buttons-container a.ty-btn.ty-btn__primary").click()
    time.sleep(2)
    print "Logging in."
    try:
        driver.find_element_by_id("login_main_login").send_keys(un)
        driver.find_element_by_id("psw_main_login").send_keys(pw)
        time.sleep(8)
        driver.find_element_by_name("dispatch[auth.login]").click()
        time.sleep(5)
        print "Logged in."
    except:
        print "Log in failed."
        driver.close()

def get_info(driver,out):
    ls = []
    try:
        name = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-detail > div.view-body > div.row-fluid.item-detailed-page > div.span5 > div.well.item-detailed-info > div.well-header.page-header > h1"))).text.encode("utf-8")
    except:
        name = "No name."
    try:
        sku = WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-detail > div.view-body > div.row-fluid.item-detailed-page > div.span5 > div.well.item-detailed-info > div.well-header.page-header > div.container-fluid > div > div:nth-child(1) > p.lead.lead-small > span > span.id > span"))).text.encode("utf-8")
    except:
        sku = "No sku."
    # try:
        # cat = "|".join([i.text.encode("utf-8") for i in driver.find_elements_by_css_selector("a.tab.search-tab")])
    # except:
        # cat = "No cat."
    try:
        desc = driver.find_element_by_css_selector("#combinedDetails").text.encode("utf-8")
    except:
        desc = "No desc."
    time.sleep(1)
    try:
        #image = driver.find_element_by_css_selector("#product-detail > div.view-body > div.row-fluid.item-detailed-page > div.span7.item-detailed-image-container > div.item-image-gallery > div > div.bx-controls.bx-has-pager.bx-has-controls-direction > div.bx-pager.bx-custom-pager > div:nth-child(1) > a > img").get_attribute("src")
        image = driver.find_element_by_css_selector("#product-detail > div.view-body > div.row-fluid.item-detailed-page > div.span7.item-detailed-image-container > div.item-image-gallery > div > img.center-block").get_attribute("src")
    except:
        try:
            image = driver.find_element_by_css_selector("#product-detail > div.view-body > div.row-fluid.item-detailed-page > div.span7.item-detailed-image-container > div.item-image-gallery > div > img.center-block").get_attribute(src)
        except:
            image = "No image."
    ls.append(name)
    ls.append(sku)
    #ls.append(cat)
    ls.append(desc)
    ls.append(image.split("?")[0])
    out.append(ls)
    print ls

	####################################
	
br = init_driver()
time.sleep(1)
br.get(url)
time.sleep(5)

table = []
items = []

with open("./csv/infile/vhc.csv","rb") as infile:
    for i in infile:
		ls = []
		print "Searching for item: " + str(i)
		## search and click
		while True:
			try:
				br.find_element_by_css_selector("input.input-medium.search-query").clear()
				br.find_element_by_css_selector("input.input-medium.search-query").send_keys(i)
				time.sleep(1)
				item = br.find_element_by_css_selector("ul.typeahead.dropdown-menu li").get_attribute("data-value").split("-")[0]
				if item == "see":
					print "Search yields no result. Displaying related results..."
					print item
					br.find_element_by_css_selector("input.input-medium.search-query").send_keys(i)
					time.sleep(1.5)
					br.find_element_by_css_selector("#item-list > div:nth-child(1) > div:nth-child(1) > div > h2 > a").click()
					print "clicked."
					time.sleep(1)
				else:
					print "Result found. " + item
					br.find_element_by_css_selector("input.input-medium.search-query").send_keys(i)
					#br.find_element_by_css_selector("#site-search-container > form > div > ul > li:nth-child(1) > a").click()
					time.sleep(1)
					get_info(br,table)
					print "clicked."
				print "Getting item attributes.."
				break
			except:
				print "Slow internet? Attempting re-search.."
				while True:
					try:
						br.refresh()
						time.sleep(1)
						break
					except:
						continue
                continue
        ## get info
		while True:
			try:
				get_info(br,table)
				break
			except:
				print "refreshing"
				br.refresh()
				time.sleep(1)
				continue
                
    # for i in set(items):
        # while True:
            # try:
                # br.get(i)
                # time.sleep(1)
                # get_info(br,table)
                # break
            # except:
                # br.refresh()
                # time.sleep(1)
                # continue
                
# br.get(bella)
# time.sleep(5)
# collections = [i.text for i in br.find_elements_by_css_selector("#default-facets-container > div:nth-child(4) > div > ul > li > h4 > a > span.name")]
# print collections


print "***Job Done***"        


        
outfile = open("./csv/outfile/vhcbrands.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)