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


URL = "http://store.shopdci.com/customer/account/login/"
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
        driver.find_element_by_name('send').click()

        print ("Login Success.")
        time.sleep(3)
 
    except:
        print "Log in failed."
        
def get_info(driver,link,out):
    print "Navigating to: \n" + str(link)
    driver.get(link)
    time.sleep(1)  
    
    try:
        sku = driver.find_element_by_css_selector("#product_addtocart_form div.product-shop div.product-name h1").text.encode("utf-8")
    except:
        sku = "No sku."

    try:
        cat = driver.find_element_by_css_selector("div.breadcrumbs").text.encode("utf-8")    
    except:
        cat = "No cat."

    try:
        dim = br.find_element_by_css_selector("div#productDetailsList").text.encode("utf-8")
    except:
        dim = "No dim."

    try:
        image = driver.find_element_by_id("image").get_attribute("src")
    except:
        image = "No image."
        

    ls = []
    

    ls.append(sku)
    
    ls.append(cat)
    
    ls.append(dim)

    ls.append(image)
    
    print ls
    
    out.append(ls)        
     
        
br = init_driver()
init_login(br,uname,pwd)
time.sleep(2)        
        
        
items = []   
table = []     
cats = []
catstring = []

# br.find_element_by_css_selector("#nav li.level0.nav-5.over a").click()
# br.get("http://store.shopdci.com/products.html/")
br.get("https://shopdci.com/Product")
time.sleep(1)

cat = br.find_elements_by_css_selector("body div div div.main-container.col1-layout div div ul.products-grid li.item div a")

for c in cat:
    itm = c.get_attribute("href")
    catstr = c.text.encode("utf-8")
    print itm
    cats.append(itm)
    catstring.append(catstr)

for x in range(len(cats)):
    br.get(cats[x])
    time.sleep(1)
    br.find_element_by_css_selector("body div div div.main-container.col2-left-layout div div.col-main div div.toolbar div.pager div.limiter select option:nth-child(4)").click()
    time.sleep(1)
    sku = br.find_elements_by_css_selector("body div div div.main-container.col2-left-layout div div.col-main div ul.products-grid li.item h2 a")
    for s in sku:
        ls = []
        ls.append(s.text.encode("utf-8"))
        ls.append(catstring[x])
        print ls
        table.append(ls)
            
print "**Items scraped**"   
    
outfile = open("./csv/outfile/dci_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"