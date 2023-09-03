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
	driver.find_element_by_css_selector("#ctl28_dvControl div div.navbar-collapse.collapse ul li:nth-child(5) a").click()
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
    sku = driver.find_element_by_id("lblItemNr").text.encode("utf-8").encode("utf-8")
    cat = "|".join(driver.find_element_by_css_selector("div.breadcrumb").text.encode("utf-8").encode("utf-8"))
    try:
        desc = driver.find_element_by_id("desc1").text.encode("utf-8").encode("utf-8")
    except:
        desc = "No desc"    
    try:
        dim = driver.find_element_by_css_selector("div.pad-10.no-pad-tb").text.encode("utf-8").split("\n")[1]
    except:
        dim = "No dim."
    try:
        set = driver.find_element_by_xpath("//*[@id=\"MainForm\"]/div[2]/section/section/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div/text()").text.encode("utf-8").encode("utf-8")
    except:
        set = "No set."
    try:
        vary = [var.text.encode("utf-8").encode("utf-8") for var in driver.find_elements_by_tag_name("option")]
        print vary[0]
    except:
        vary = "No option"
    try:
        qty = driver.find_element_by_name("txtQuantity").get_attribute("value")
    except:
        qty = "No min qty."
    price = driver.find_element_by_id("lblPrice").text.encode("utf-8").encode("utf-8")
    try:
        image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a.main-product-photo.block.zoom.rel"))).get_attribute("href")
    except:
        image = "No image."
    try:
        if vary[0] == "Please Select Size":
            for i in vary:
                ls = []
                ls.append(name.text.encode("utf-8").encode("utf-8"))
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
            ls.append(name.text.encode("utf-8").encode("utf-8"))
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
        ls.append(name.text.encode("utf-8").encode("utf-8"))
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
        
# br = init_driver()
# br.get(url)
# time.sleep(2)
# init_login(br,uname,passw)
# time.sleep(2)


sections = []
items = []

# tree = tree.parse("./csv/infile/2018 Craft Outlet products updated_Product.xml")

# for node in tree.iter():
    # if node.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}loc":
        # print node.text.encode("utf-8")
        
# links = [node.text.encode("utf-8") for node in tree.iter() if node.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"]
# print len(links)


    
tree = tree.parse("./csv/infile/sitemap.xml")

# for node in tree.iter():
	# time.sleep(1)
	# print dir(node)
	# print node
	# print "Attrib:"+str(node.attrib)
	# print "Text:"+str(node.text.encode("utf-8"))
	# print "Tag:" +node.tag
	
	
# nodes = [node for node in tree.iter()]
# for node in nodes:
	# print node.tag
	
final = []
prod = tree.findall("Product")
for p in prod:
	try:
		d = p.find("description").text.encode("utf-8")
	except:
		d = ""
	sku = p.find("item_no").text.encode("utf-8")
	try:
		qty1 = p.find("qty_min").text.encode("utf-8")
	except:
		qty1 = ""
	try:
		qty2 = p.find("qty_break1").text.encode("utf-8")
	except:
		qty2 = ""
	try:
		qty3 = p.find("qty_break2").text.encode("utf-8")
	except:
		qty3 = ""
	try:
		price1 = p.find("price1").text.encode("utf-8")
	except:
		price1 = ""
	try:
		price2 = p.find("price2").text.encode("utf-8")
	except:
		price2 = ""
	try:
		price3 = p.find("price3").text.encode("utf-8")
	except:
		price3 = ""
	try:
		upc = p.find("item_upc").text.encode("utf-8")
	except:
		upc = ""
	
	final.append([d,sku,qty1,qty2,qty3,price1,price2,price3,upc])
	
outfile = open("./csv/outfile/packagingsource_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(final)
outfile.close()

print "Done"