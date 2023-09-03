from selenium import webdriver
import xml.etree.ElementTree as tree
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



url = "http://www.packagingsource.com/"
xmlpage = "https://www.packagingsource.com/sitemap.xml"
uname = "rick@waresitat.com"
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser
    
def init_login(driver,un,pw):
	print "Logging in..."
	driver.find_element_by_css_selector("div > div.navbar-collapse.collapse > ul > li:nth-child(6) > a").click()
	time.sleep(1)
	driver.find_element_by_name("txtEmailAddress").send_keys(un)
	driver.find_element_by_name("txtPassword").send_keys(pw)
	driver.find_element_by_name("btnSignIn").click()
	time.sleep(3)
	print "Success."
    
def get_items(driver,out):
    print "\nEvent: Showing all items.\n"
    driver.find_element_by_css_selector("#ddShowByPageSize option:nth-child(5)").click()
    time.sleep(2)
    out.extend([i.get_attribute("href") for i in driver.find_elements_by_css_selector("div.no-m-b a") if i.get_attribute("href") != "http://www.packagingsource.com/store/Catalog-Request.html"])
    it = [i.get_attribute("href") for i in driver.find_elements_by_css_selector("div.no-m-b a") if i.get_attribute("href") != "http://www.packagingsource.com/store/Catalog-Request.html"]
    for i in it:
        print i
    print "\nStatus: Product links pushed to memory.\n"

def get_items_section(driver,out):
    while True:
        try:
            item = [itm.get_attribute("href") for itm in driver.find_elements_by_css_selector("div.CategoryCategoryThumbnail a") if i != "http://www.packagingsource.com/store/Catalog-Request.html"]
            for itm in item:
                print "\nEvent: Navigating to link for more products.:\n" + itm
                driver.get(itm)
                time.sleep(1)
                get_items(driver,out)
            break
        except Exception as e:
            print e
            time.sleep(1)
            continue
            
def search(driver,keyword):
    while True:
        
            #enter keyword
            try: 
                print "Searching for item: " + i
                driver.find_element_by_css_selector("div > div.navbar-collapse.collapse > div > ul > li:nth-child(1)").click()
                driver.find_element_by_name("txtRedirectSearchBox").send_keys(i)
                time.sleep(1)
                break
            except Exception as x:
                print "Search failed. Printing error: " + str(x)
                time.sleep(1)
                driver.get("http://www.packagingsource.com/")
                time.sleep(5)
	
def get_info(driver,link,out):
    if link != "http://www.packagingsource.com/store/Catalog-Request.html":
        print "\nEvent: Navigating to link to get attributes:\n " + str(link)
        driver.get(link)
        time.sleep(1)
    name = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h1.ProductDetailsProductName.no-m-t")))
    sku = driver.find_element_by_id("lblItemNr").text.encode("utf-8")
    cat = "|".join([i.text for i in driver.find_elements_by_css_selector("div.breadcrumb a")])
    try:
        desc = driver.find_element_by_id("desc1").text.encode("utf-8")
    except:
        desc = "No desc"    
    try:
        dim = driver.find_element_by_css_selector("div.pad-10.no-pad-tb").text.split("\n")[1]
    except:
        dim = "No dim."
    try:
        set = driver.find_element_by_xpath("//*[@id=\"MainForm\"]/div[2]/section/section/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div/text()").text.encode("utf-8")
    except:
        set = "No set."
    try:
        vary = [var.text.encode("utf-8") for var in driver.find_elements_by_tag_name("option")]
        print vary[0]
    except:
        vary = "No option"
    try:
        qty = driver.find_element_by_name("txtQuantity").get_attribute("value")
    except:
        qty = "No min qty."
    price = driver.find_element_by_id("lblPrice").text.encode("utf-8")
    try:
        image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a.main-product-photo.block.zoom.rel"))).get_attribute("href")
    except:
        image = "No image."
    try:
        if vary[0] == "Please Select Size":
            for i in vary:
                ls = []
                ls.append(name.text.encode("utf-8"))
                ls.append(i)
                ls.append(sku)
                ls.append(cat)
                ls.append(desc)
                ls.append(dim)
                ls.append(set)
                ls.append(qty)
                ls.append(price)
                ls.append(image)
                print ls
                out.append(ls)
        else:
            ls = []
            ls.append(name.text.encode("utf-8"))
            ls.append("|".join(vary))
            ls.append(sku)
            ls.append(cat)
            ls.append(desc)
            ls.append(dim)
            ls.append(set)
            ls.append(qty)
            ls.append(price)
            ls.append(image)
            print ls
            out.append(ls)
    except:
        ls = []
        ls.append(name.text.encode("utf-8"))
        ls.append(vary)
        ls.append(sku)
        ls.append(cat)
        ls.append(desc)
        ls.append(dim)
        ls.append(set)
        ls.append(qty)
        ls.append(price)
        ls.append(image)
        print ls
        out.append(ls)
        
br = init_driver()
br.get(url)
time.sleep(2)
init_login(br,uname,passw)
time.sleep(2)


sections = []
items = []

tree = tree.parse("./csv/infile/sitemap.xml")
links = [node.text for node in tree.iter() if node.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"]

		
# cats = [i.get_attribute("href") for i in br.find_elements_by_css_selector("a.category-link")]

# for itm in cats:
    # print "Navigating to: " + str(itm)
    # br.get(itm)
    # time.sleep(1)
    # try:
        # sections.extend([i.get_attribute("href") for i in br.find_elements_by_css_selector("div.CategoryCategoryThumbnail a")])
        # for section in sections:
            # print section
    # except:
        # if (itm == "http://www.packagingsource.com/Gift-Wrap-FREE-FREIGHT.html" or itm == "http://www.packagingsource.com/store/c/4059-Gift-Wrap-Stewo.html" or itm == "http://www.packagingsource.com/Labels-Designer.html" or itm == "http://www.packagingsource.com/Wraphia-Raffia.html"):
            # sections.append(itm)
            # print "\nStatus: The following link has already items in it.\n"
            # print itm
            # time.sleep(1)
            
# items = []
		
# for i in sections:
    # print "Navigating to: " + str(i)
    # br.get(i)
    # time.sleep(1)
    # while True:
        # try:
            # print "\nStatus: Push product links to memory..\n"
            # get_items(br,items)
            # break
        # except:
            # print "\nStatus: More items found. Navigating each for more items..\n"
            # time.sleep(1)
            # get_items_section(br,items)

table = []

for i in set(links):
    count = 0;
    while True:
        try:
            if count > 3:
				break
            get_info(br,i,table)
            break
        except Exception as e:
            count += 1
            print e
            br.refresh()
            continue
            
# table = []
# with open("./csv/infile/packagingsource.csv","rb") as infile:
    # for i in infile:
        # ActionChains(br).move_to_element(br.find_element_by_css_selector("div > div.navbar-collapse.collapse > div > ul > li:nth-child(1)")).perform()
        # br.find_element_by_css_selector("div > div.navbar-collapse.collapse > div > ul > li:nth-child(1)").click()
        # time.sleep(1)
            
            
        # while True:
            # search(br,i)
            # if page error detected, go back
            # try:
                # br.find_element_by_id("lblAppException")
                # continue
            # except:
                # product page detection
                # if br.current_url.split("/")[4].strip() == "p":
                    # print "Getting current url.\n"
                    # items.append(br.current_url)
                    # print br.current_url
                    # time.sleep(1)
                    # break
                # else:
                # multiple product detection
                    # get_items(br,items)
                    # time.sleep(1)
                    # break
                    
# for item in set(items):
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
			
print "***Job Done***"

outfile = open("./csv/outfile/thepackagingsource_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()