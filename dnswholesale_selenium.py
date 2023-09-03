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

login = "http://www.dnsdesignsandmore.com/index.php?route=account/login"
url = "http://www.dnsdesignsandmore.com/index.php"
uname = "rick@waresitat.com"
pw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
    
def init_login(driver,un,passw):
    driver.get(login)
    print "Logging in."
    try:
        driver.find_element_by_name("email").send_keys(un)
        driver.find_element_by_name("password").send_keys(pw)
        driver.find_element_by_css_selector("#content > div.login-content > div.right > form > div > input.button").click()
        time.sleep(1)
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
        

                                      
br = init_driver()
init_login(br,uname,pw)
br.get(url)
time.sleep(1)



items = []
table = []


# links = [i.get_attribute("href") for i in br.find_elements_by_css_selector("#menu > ul > li > div > ul > li > a")]

# for link in links:
    # print "Getting all items in " + link
    # br.get(link)
    # time.sleep(1)
    # show 100 items
    # try:
        # br.find_element_by_css_selector("#content > div.product-filter > div.limit > select > option:nth-child(5)").click()
        # time.sleep(1)
        # items.extend([i.get_attribute("href") for i in br.find_elements_by_css_selector("#content > div.product-list > div > div.left > div.name > a")])
        # while True:
            # try:
                # br.find_element_by_link_text(">").click()
                # time.sleep(1)
                # items.extend([i.get_attribute("href") for i in br.find_elements_by_css_selector("#content > div.product-list > div > div.left > div.name > a")])
            # except:
                # print "Status: Pagination exhausted."
                # break
    # except:
        # print "Category empty."
with open("./csv/infile/dnswholesale.csv","rb") as infile:
    for i in infile:
        br.find_element_by_name("filter_name").clear()
        br.find_element_by_name("filter_name").send_keys(i)
        time.sleep(1)
        try:
            item = br.find_elements_by_css_selector("div.name a")
            for i in item:
				if((i.get_attribute("href")).endswith("=")):
					break
				else:
					items.append(i.get_attribute("href"))
					print i.get_attribute("href")
        except:
            print "No item found. Searching for next item..."


for i in set(items):
    # try:
    ls = []
    print "Status: Navigating to " + i
    br.get(i)
    time.sleep(1)
    sku = br.find_element_by_css_selector("div.description").text.encode("utf-8")
    cat = "|".join([i.text.encode("utf-8") for i in br.find_elements_by_css_selector("div.breadcrumb a")])
    image = br.find_element_by_css_selector("div.image a").get_attribute("href")

    ls.append(sku)
    ls.append(cat)
    ls.append(image)
    table.append(ls)
    print ls
    # except:
        # print "Product not found."
                
        
outfile = open("./csv/outfile/dnswholesale_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"