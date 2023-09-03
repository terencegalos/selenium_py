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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import text_generator_cat_maker as catmaker

caps = DesiredCapabilities.FIREFOX





# Tell the Python bindings to use Marionette.
# This will not be necessary in the future,
# when Selenium will auto-detect what remote end
# it is talking to.
caps["marionette"] = True

url = "https://www.waresitat.com/waresitat.cfm"
destination = "https://www.waresitat.com/vendor_detail.cfm?VendorID=8042"
uname = "canada2"
passw = "2"

def init_driver():
    path = "./chrome_driver/chromedriver"
    #path = "./firefox_driver/geckodriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_name("login_username").send_keys(un)
    driver.find_element_by_name("password").send_keys(pw)
    driver.find_element_by_name("password").send_keys(Keys.RETURN)
    time.sleep(1)
    print "Logged in."


        
br = init_driver()
init_login(br,uname,passw)
time.sleep(1)
br.get(destination)
time.sleep(1)

items = []
table = []

cat = br.find_elements_by_css_selector("#right_content div.display_vendor div table tbody tr td a")
cats = [cat.get_attribute("href") for cat in br.find_elements_by_css_selector("#demo > div > ul > li > a:nth-child(2)")]
    
def scrape_page(driver,out):
    products = driver.find_elements_by_css_selector("#vendor_shop > div")
    for product in products:
		ls = []
		name = product.find_element_by_css_selector("form > div.product_desc_home > div.scrolldescription > input[type=\"hidden\"]:nth-child(3)").get_attribute("value")
		sku = product.find_element_by_css_selector("form > div.product_desc_home > div.scrolldescription").text.split("\n")
		try:
			stock = product.find_element_by_css_selector("#vendor_shop > div:nth-child(3) > form > div.product_desc_home > div.scrolldescription > span.soldout").text.encode("utf-8")
		except:
			stock = "No stock status."
		pic = product.find_element_by_css_selector("form > div.product_thumb_home > div.outerdivcatimgbox > div > a > img").get_attribute("src").split("/")[-1:]
		qty = product.find_element_by_css_selector("input[name=\"prod_qty\"]").get_attribute("value")
		ls.append(name.encode("utf-8"))
		ls.append(sku[3].encode("utf-8"))
		ls.append(driver.find_element_by_css_selector("#right_content > div.col-lg-7.col-md-7.col-sm-6 > h1").text.encode("utf-8"))
		ls.append(stock)
		ls.append(sku[2].encode("utf-8"))
		ls.append(qty)
		ls.append(sku[1].encode("utf-8"))
		ls.append(pic[0].encode("utf-8"))
		out.append(ls)
		#print ls

    
    

for x in range(len(cats)):
    print "Navigating to: " + str(cats[x])
    br.get(cats[x])
    time.sleep(3)
    scrape_page(br,table)
    while True:
        try:
            br.find_element_by_link_text("next page").click()
            time.sleep(2)
            scrape_page(br,table)
        except:
            print "Pagination exhausted"
            break
                

skus = [row[1] for row in table]
print skus
time.sleep(5)
final = catmaker.make_cats(set(skus),table)
finaltable = []


for line in final:
	for row in table:
		#print row
		if line[0].strip() == row[1].strip():
			#print "Match found."
			try:
				prod = [row[0],row[1],line[1].strip(),row[3],row[4],row[5],row[6],row[7]]
				print prod
				finaltable.append(prod)
				#break when match found (avoid duplicates)
				break
			except Exception as e:
				print e
				print line[1]
				print row
				time.sleep(5)
			
print finaltable				
			


outfile = open("./csv/outfile/waresitat_kraftklub.csv","wb")
writer = csv.writer(outfile)
writer.writerows(finaltable) 

print "**Job Done***"
br.close()