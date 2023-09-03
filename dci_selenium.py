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

URL = "https://shopdci.com/"
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
	driver.find_element_by_css_selector("#pre-login-navbar > li.signIn-li > a").click()
	time.sleep(1)
	#driver.find_element_by_css_selector("#paragraphs > p:nth-child(3) > strong > a").click()
	time.sleep(1)
	
	print "Logging in..."
	driver.find_element_by_name('LogonEmail').send_keys(un)
	driver.find_element_by_name('LogonPassword').send_keys(pw)
	driver.find_element_by_name('LogonPassword').send_keys(Keys.ENTER)
	
	print ("Login Success.")
	time.sleep(3)
		
def get_info(driver,out):
    # print "Navigating to: \n" + str(link)
    # driver.get(link)
    # time.sleep(1)  
    
    try:
        sku = driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > div.productDetail-item-pnumber > span:nth-child(2)").text.encode("utf-8")
    except:
        sku = "No sku."

    # try:
        # cat = driver.find_element_by_css_selector("div.breadcrumbs").text.encode("utf-8")    
    # except:
        # cat = "No cat."

    # try:
        # dim = br.find_element_by_css_selector("div#productDetailsList").text.encode("utf-8")
    # except:
        # dim = "No dim."

    try:
        image = driver.find_element_by_css_selector("#product-detail-main-image").get_attribute("src")
    except:
        image = "No image."
        

    ls = []
    

    ls.append(sku)

    ls.append(image)
    
    print ls
    
    out.append(ls)        
     
        
br = init_driver()
init_login(br,uname,pwd)
        
#br.get("https://shopdci.com/Trade/Access")
time.sleep(1)        
        
items = []
table = []     

with open("./csv/infile/dci.csv","rb") as infile:
	for i in infile:
		print "Searching for " + str(i) + "\n"
		br.find_element_by_css_selector("#filter-searchString").clear()
		br.find_element_by_css_selector("#filter-searchString").send_keys(i)
		time.sleep(10)
		
		#btn = br.find_element_by_css_selector("#product-list-container > div:nth-child(5) > div.product-item-container.center-block.selected > div.product-item-image.row")
		btn = br.find_element_by_css_selector("#product-list-container > div:nth-child(5) > div.product-item-container.center-block > div.product-description.row")
		print btn.get_attribute('innerHTML')
		btn.click()
		#br.find_element_by_css_selector("#product-list-container > div:nth-child(5) > div.product-item-container.center-block.selected > div.product-item-image.row").click()
		time.sleep(2)
		get_info(br,table)

            
print "**Items scraped**"
    
outfile = open("./csv/outfile/dci_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"