from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv


BASE_URL = "https://www.rowepottery.com/"
URL = "https://www.rowepottery.com/customer/account/login/"
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
    try:
        print "Logging in..."
        driver.find_element_by_name('login[username]').send_keys(un)
        driver.find_element_by_name('login[password]').send_keys(pw)
        driver.find_element_by_id('send2').click()

        print ("Login Success.")
 
    except:
        print "Login failed."

def get_items_url():
    #wait for product urls
    rawitems = WebDriverWait(br, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-title")))
    #getting each products url
    for i in range(len(rawitems)):
        print "Getting item: " + str(i)  
        items.append(rawitems[i].get_attribute('href'))
        print "Item acquired."
    
        
br = init_driver()
#log in
init_login(br,uname,pwd)



#get all categories
rawcats = WebDriverWait(br, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "level0")))



#get all categories' href value
cats = []
catss = []
for i in range(len(rawcats)):
    cats.append(rawcats[i].get_attribute('href'))
    print "Getting next category..."    
    
    
#navigate to each category page and get pagination
for cat in cats:
    print "**Navigating to category: " + cat
    br.get(cat)
    print "**Loaded."
    
    page = br.find_elements_by_class_name("pages")
    pages = []
    
    #divide list by 2 and append to a new list
    for i in range(len(page)/2):
        pages.append(page[i].get_attribute("href"))
    
    print "**Number of pages: " + str(len(pages))
    
    #get all pagination
    for i in range(len(pages)):
        print "Getting pages for category - " +cat+ " \nPage: " +str(i+1)+ "\n"
        catss.append(pages[i])
 
    #find more pages and append
    try:
        if page[((len(page))/2)-1].text == "...":
            print "More pages found. Clicking..."
            br.get(page[((len(page))/2)-1].get_attribute('href'))
            morepage = br.find_elements_by_name("pagination")
            for i in morepage:
                if i not in catss:
                    print "Appending " + str(i.get_attribute("href")) + " to catss"
                    catss.append(i.get_attribute("href"))
                else:
                    print str(i) + " not in catss."
    except:
        print "No further pages found."
    
                
            

#adding all pages
for i in cats:
    catss.append(i)
list(set(catss))
#get all items in all pages
items = []
for i in range(len(catss)):
    print i
    br.get(str(catss[i]))
    get_items_url()
     
#scrape each items' attribute to a table
table = []
for item in items:

    ls = []
    print "Navigating to item: " + item
    br.get(item)
    print "Getting product attributes..."
    try:
        title = br.find_element_by_class_name("mainbox-title")
        sku = br.find_element_by_class_name("sku")
        section = br.find_element_by_class_name("breadcrumbs")
        price = br.find_element_by_class_name("price")
        desc = br.find_element_by_id("content_block_description")
        desc2 = br.find_element_by_class_name("description")
    except:
        print "Something's missing.."
    image = br.find_element_by_class_name("cm-thumbnails")
    
    ls.append(title.text.encode("utf-8"))
    ls.append(sku.text.encode("utf-8"))
    ls.append(section.text.encode("utf-8"))
    ls.append(price.text.encode("utf-8"))
    try:
        ls.append(desc.text.encode("utf-8"))
    except:
        print "Value empty. Appending 'None' instead"
        ls.append("None")
    try:
        ls.append(desc2.text.encode("utf-8"))
    except:
        print "Value empty. Appending 'None' instead."
        ls.append("None")
    ls.append(image.get_attribute('src'))
    table.append(ls)
    print "Printing product attributes: "
    print ls

#make a csv file and write
outfile = open("./csv/hearthsideitems.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)