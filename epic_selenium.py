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
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
    
def init_login(driver,un,pw):
    print "Logging in..."
    driver.find_element_by_link_text("Login").click()
    time.sleep(1)
    try:
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME,"EMail"))).send_keys(un)
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME,"txtPassword"))).send_keys(pw)
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME,"LoginButton"))).click()
        time.sleep(5)
        print "Success."
    except:
        print "Failed."
        driver.close()
        
        
def get_items(driver,out):
	#get items the first time
	it = [i.get_attribute("href") for i in driver.find_elements_by_css_selector("#content table tbody tr td:nth-child(2) table tbody tr:nth-child(2) td table tbody tr:nth-child(7) td table tbody tr:nth-child(1) td table tbody tr td table tbody tr td.product-grid-text a")]
	for i in list(set(it)):
		out.append(i)
		print i

def get_info(driver,link,out):
    driver.get(link)
    time.sleep(1)
    name = driver.find_element_by_css_selector("td.product-name").text.encode("utf-8")
    sku = driver.find_element_by_css_selector("#content table tbody tr td:nth-child(2) table:nth-child(2) tbody tr:nth-child(2) td table tbody tr:nth-child(7) td table tbody tr:nth-child(1) td table tbody tr td.product-details div:nth-child(3)").text.encode("utf-8")
    cat = driver.find_element_by_id("breadcrumb").text.encode("utf-8")
    desc = driver.find_element_by_css_selector("td.product-description").text.encode("utf-8")
    dim = driver.find_element_by_css_selector("#content table tbody tr td:nth-child(2) table:nth-child(2) tbody tr:nth-child(2) td table tbody tr:nth-child(7) td table tbody tr:nth-child(1) td table tbody tr td.product-details div:nth-child(9)").text.encode("utf-8")
    image = br.find_element_by_css_selector("#content table tbody tr td:nth-child(2) table:nth-child(2) tbody tr:nth-child(2) td table tbody tr:nth-child(7) td table tbody tr:nth-child(1) td table tbody tr td:nth-child(1) div div img").get_attribute("src")
    
    ls = []
    ls.append(name)
    ls.append(sku.split()[1])
    ls.append(cat)
    ls.append(desc)
    ls.append(dim)
    ls.append(image)
    out.append(ls)
    print "\n"
    print [s for s in ls]
    print "\n"
        
###################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

br = init_driver()
time.sleep(1)
br.get("http://www.epicproductsinc.com/default.aspx")
time.sleep(1)
init_login(br,uname,passw)
time.sleep(1)
table = []

# #get categories
# cat = [s.get_attribute("href") for s in br.find_elements_by_css_selector("#qm0 div a")]
# items = []
# table = []

# #iterate each get and subcategory or items
# for c in list(set(cat)):
    # print "Navigating to " + c
    # #check subcategory found
    # if c == "http://www.epicproductsinc.com/c-421-holiday-collections.aspx" or c == "http://www.epicproductsinc.com/c-422-everyday-collections.aspx":
        # br.get(c)
        # time.sleep(1)
        # subcats = [ct.get_attribute("href") for ct in br.find_elements_by_css_selector("#content table tbody tr td:nth-child(2) table tbody tr:nth-child(2) td table tbody tr:nth-child(7) td table tbody tr:nth-child(1) td table tbody tr td table tbody tr td a")]
        # print "Subcategory found. Navigating each"
        # for item in list(set(subcats)):
            # print "Navigating subcategory " + item
            # if item == "http://www.epicproductsinc.com/c-320-santa-rocks-collection.aspx":
                # print "Skipping.."
            # else:
                # try:
                    # br.get(item)
                    # time.sleep(3)
                    # get_items(br,items)
                # except:
                    # print "Skipped."
    # #if no subcategory
    # else:
        # try:
            # br.get(c)
            # print "No subcategory. Getting items immediately..."
            # get_items(br,items)
            # time.sleep(1)
        # except:
            # print "Skipped."

# ulist = list(set(items))

# outfile1 = open("./csv/outfile/epic_items.csv","wb")
# writer = csv.writer(outfile1)
# writer.writerow(ulist)

with open("./csv/infile/epic_items.csv","rb") as infile:
    for item in infile:
		i = item.split(",")
		for prod in i:
			get_info(br,prod,table)
	

outfile = open("./csv/outfile/epic_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"
br.close()