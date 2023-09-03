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

url = "http://www.janmichaelscrafts.com/"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    btn = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#TopMenu ul li:nth-child(4) div a:nth-child(1)")))
    btn.click()
    time.sleep(1)
    print "Logging in."
   
    driver.find_element_by_id("login_email").send_keys(un)
    driver.find_element_by_id("login_pass").send_keys(pw)
    driver.find_element_by_id("LoginButton").click()
    time.sleep(5)
    print "Success."
    
def get_info(driver,i,out):
    ls = []
    while True:
        try:
            driver.get(i)
            break
        except:
            br.refresh()
            time.sleep(1)
            continue
    print "Navigating to:\n" + str(i)
    
    time.sleep(1)
    title = driver.find_element_by_css_selector("h2.title").text.encode("utf-8")
    sku = driver.find_element_by_css_selector("#productDetailsAddToCartForm div div.DetailRow.ProductSKU div.Value span").text.encode("utf-8")
    min = driver.find_element_by_css_selector("select option:checked").get_attribute("value")
    try:
        origprice = driver.find_element_by_css_selector("#ProductDetails > div > div.ProductMain > div.ProductDetailsGrid > div.p-price > div.DetailRow.PriceRow > div > em.ProductPrice.RetailPrice.on-sale > strike").text.encode("utf-8")
    except:
        origprice = "No origprice"
    desc = driver.find_element_by_css_selector("#ProductDescription div").text.encode("utf-8")
    try:
        price = driver.find_element_by_css_selector("#ProductDetails div div.ProductMain div.ProductDetailsGrid div.p-price div.DetailRow.PriceRow div em.ProductPrice.VariationProductPrice").text.encode("utf-8")
    except:
        price = driver.find_element_by_css_selector("#ProductDetails > div > div.ProductMain > div.ProductDetailsGrid > div.p-price > div.DetailRow.PriceRow > div > em.ProductPrice.VariationProductPrice.on-sale").text.encode("utf-8")
    
    ActionChains(driver).move_to_element(driver.find_element_by_css_selector("#TinyImage_0")).perform()
    time.sleep(1)
    
    #image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ProductDetails div div.left-content div.ProductThumb div.ProductThumbImage a div.zoomie img"))).get_attribute("src")
    image = driver.find_element_by_css_selector("#ProductDetails div div.left-content div.ProductThumb div.ProductThumbImage a div.zoomie img").get_attribute("src")

    ls.append(title)
    ls.append(sku)
    ls.append(desc)
    ls.append(min)
    ls.append(price)
    ls.append(origprice)
    ls.append(image)
    out.append(ls)
    print ls
    try:
        option = [btn.text.encode("utf-8") for btn in driver.find_elements_by_css_selector("div.productAttributeValue > div > ul > li > label > span.name")]
        print option
        print "Status: More options detected."
        time.sleep(1)
        for x in range(len(option)):
            print x
            ls = []
            driver.find_elements_by_css_selector("div.productAttributeValue > div > ul > li")[x].click()
            time.sleep(2)
            
            sku = driver.find_element_by_css_selector("#productDetailsAddToCartForm div div.DetailRow.ProductSKU div.Value span").text.encode("utf-8")
            try:
                price = driver.find_element_by_css_selector("#ProductDetails div div.ProductMain div.ProductDetailsGrid div.p-price div.DetailRow.PriceRow div em.ProductPrice.VariationProductPrice").text.encode("utf-8")
            except:
                price = driver.find_element_by_css_selector("#ProductDetails > div > div.ProductMain > div.ProductDetailsGrid > div.p-price > div.DetailRow.PriceRow > div > em.ProductPrice.VariationProductPrice.on-sale").text.encode("utf-8")
            
            ls.append(title)
            ls.append(sku)
            ls.append(desc)
            ls.append(price)
            ls.append(origprice)
            ls.append(image)
            out.append(ls)
            print ls
    except Exception as e:
        print e
        time.sleep(1)
         

br = init_driver()
br.get(url)
time.sleep(2)
init_login(br,uname,passw)

table = []
items = []
sale = "http://www.janmichaelscrafts.com/clearance/"
cats = []

# cats.extend([i.get_attribute("href") for i in br.find_elements_by_css_selector("#SideCategoryList > div > div > ul > li > a")])
# for cat in cats[:-1]:
    # br.get(cat)
    # time.sleep(1)
    # for item in br.find_elements_by_css_selector("a.pname"):
        # link = item.get_attribute("href")
        # print link
        # items.append(link)
    # print "\nGetting all pages for more products...\n"
    # time.sleep(1)
    # while True:
        # try:
            # br.find_element_by_css_selector("a.nav-next").click()
            # print "Event: Next page clicked."
            # time.sleep(1)
            # for item in br.find_elements_by_css_selector("a.pname"):
                # link = item.get_attribute("href")
                # print link
                # items.append(link)
        # except:
            # break
    # print "\nStatus: This category has been scraped out of items. Proceeding...\n"
    # time.sleep(1)
            
with open("./csv/infile/janmichaelcrafts.csv","rb") as infile:
    for i in infile:
        print "Searching for " + i
        while True:
            try:
                br.find_element_by_name("search_query").clear()
                br.find_element_by_name("search_query").send_keys(i.strip()+" ")
                time.sleep(2.5)
                break
            except:
                br.refresh()
                time.sleep(1)
                continue
		# while True:
			# try:
				# item = [x.get_attribute("href") for x in br.find_elements_by_css_selector("#frmCompare > div.SearchContainer > ul > li > div.ProductDetails.cf > p.p-name > a")]
				# break
			# except:
				# br.refresh()
				# time.sleep(1)
				# continue
        try:
            item = br.find_element_by_css_selector("table.QuickSearch a:nth-child(1)").get_attribute("href")
            print "Link found: " + str(item)
            items.append(item)    
        except:
            print "Item not found."


for itm in set(items):
    while True:
        try:
            get_info(br,itm,table)
            break
        except Exception as e:
            print e
            br.refresh()
            time.sleep(1)
            continue

print "***Job Done***"        
        
outfile = open("./csv/outfile/janmichaelscrafts_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()