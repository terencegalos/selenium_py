from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

url = "http://www.pdhomemarket.com/"
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
    title = driver.find_element_by_css_selector("#product_description").text.encode("utf-8")
    sku = driver.find_element_by_css_selector("#v65-product-parent > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div > i > font > span.product_code").text.encode("utf-8")
    cat = "|".join([i.text.encode("utf-8") for i in driver.find_elements_by_css_selector("#v65-product-parent > tbody > tr:nth-child(1) > td > b > a")])
    min = driver.find_element_by_css_selector("#v65-productdetail-action-wrapper > table:nth-child(1) > tbody > tr > td:nth-child(1) > input").get_attribute("value")
    
    #image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ProductDetails div div.left-content div.ProductThumb div.ProductThumbImage a div.zoomie img"))).get_attribute("src")
    try:
        image = driver.find_element_by_css_selector("#product_photo_zoom_url").get_attribute("href")
    except:
        image = "No image found."

    ls.append(title)
    ls.append(sku)
    ls.append(cat)
    ls.append(min)
    ls.append(image)
    out.append(ls)
    print ls

br = init_driver()
br.get(url)
time.sleep(2)
#init_login(br,uname,passw)

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
            
with open("./csv/infile/pdhomeandgarden_sku.csv","rb") as infile:
    for i in infile:
        print "Searching for " + i
        while True:
            try:
                br.find_element_by_name("Search").clear()
                br.find_element_by_name("Search").send_keys(i.strip())
                br.find_element_by_name("Search").send_keys(Keys.RETURN)
                time.sleep(2.5)
                break
            except Exception as s:
                print s
                br.refresh()
                time.sleep(1)
                continue
        try:
            item = br.find_element_by_css_selector("#MainForm > table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > div > div > div > div > a").get_attribute("href")
            print "Link found: " + str(item)
            items.append(item)    
        except:
            print "Item not found."


for itm in set(items):
    get_info(br,itm,table)
    # while True:
        # try:
            # break
        # except Exception as e:
            # print e
            # br.refresh()
            # time.sleep(1)
            # continue

print "***Job Done***"        
        
outfile = open("./csv/outfile/pdhomeandgarden_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()