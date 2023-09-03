from selenium import webdriver
import time
import urllib2
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from urllib import urlopen
import urllib
import csv

url = "http://www.lizbethjanedesigns.com/"
uname = "waresitat"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):    
    driver.get("http://lizbeth.cameoez.com/Scripts/PublicSite/?template=Login")
    time.sleep(2)
    try:
        print "Logging in..."
        driver.find_element_by_name('username').send_keys(un)
        driver.find_element_by_name('password').send_keys(pw)
        driver.find_element_by_css_selector("#loginWrapper tbody tr:nth-child(2) td:nth-child(1) form table tbody tr:nth-child(3) td:nth-child(2) input[type=\"submit\"]").click()
        print "Login Success."
    except:
        print "Login failed."
        br.close()
        
def get_items(driver,container):
    print "Getting all items in this page..."
    item = driver.find_elements_by_css_selector("a.popup.cboxElement")
    catlink = []
        
    for it in item:
        print [it.get_attribute("href")]
        catlink.append(it.get_attribute("href"))
        try:
            select = Select(driver.find_element_by_name("subCat"))
            cattext = select.first_selected_option
            print cattext.text
            catlink.append(cattext.text.encode("utf-8").strip())
        except:
            print "No category to insert in a list."
		
        print catlink
        container.append(catlink)
        catlink = []
        
def get_attribute(driver,link,container,item_category):
    driver.get(link)
    time.sleep(1)
    name = driver.find_element_by_css_selector("#popupwrapper table tbody tr td.itemName").text.encode("utf-8")
    price = driver.find_element_by_css_selector("#descCell p.price").text.encode("utf-8")
    sku = driver.find_element_by_css_selector("#descCell p.sku").text.encode("utf-8")
    option = driver.find_element_by_css_selector("#descCell p.options")
    opt = option.find_elements_by_css_selector("select option")
    image = driver.find_element_by_css_selector("#imgCell img").get_attribute("src")
    try:
        for op in opt:
            ls = []
            ls.append(name)
            ls.append(sku.split()[1])
            ls.append(item_category)
            ls.append(op.text.encode("utf-8"))
            ls.append(price.split("/")[1])
            ls.append(price.split("/")[0])
            ls.append(image)
            print ls
            container.append(ls)
    except:
        ls = []
        ls.append(name)
        ls.append(sku.split()[1])
        ls.append(item_category)
        ls.append("No option.")
        ls.append(price.split("/")[1])
        ls.append(price.split("/")[0])
        ls.append(image)
        container.append(ls)
        print ls
        
    

def paginator(driver,container):
	while True:
		try:
			driver.find_element_by_css_selector("#pageNav tbody tr td:nth-child(3) a").click()
			print "Next page click3d...."
			time.sleep(1)
			get_items(driver,container)
		except:
			print "Next page exhausted."
			break
            

#initialize and open browser
br = init_driver()
br.get(url)
time.sleep(1)
init_login(br,uname,passw)
time.sleep(2)

table = []
items = []


with open("./csv/infile/lizbeth_items.csv","rb") as infile:
    for i in infile:
        it = i.split(",")
        print it
        get_attribute(br,it[0],table,it[1])
        time.sleep(1)

outfile = open("./csv/outfile/lizbethjanedesigns_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)        
br.close()