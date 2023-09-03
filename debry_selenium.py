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


url = "http://www.debrycompany.com/index.php/"
uname = "rick@waresitat.com"
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_link_text("Log In").click()
    time.sleep(1)
    print "Logging in."
    
    driver.find_element_by_name("login[username]").send_keys(un)
    driver.find_element_by_name("login[password]").send_keys(pw)
    driver.find_element_by_name("send").click()
    time.sleep(5)
    print "Logged in."

def get_info(driver,link,out):
    print "Navigating to: \n" + str(link)
    driver.get(link)
    time.sleep(1)

    try:
        name = driver.find_element_by_css_selector("#product_addtocart_form div.product-shop div.product-name h1").text.encode("utf-8")
    except:
        name = "No name."
    
    try:
        skus = []
        sku = driver.find_elements_by_css_selector("#product-options-wrapper dl dd select option")
        for i in sku:
            sk = i.text.encode("utf-8")
            print sk
            skus.append(sk)
    except:
        skus = "No sku."
    
    try:
        desc = driver.find_element_by_css_selector("#product_tabs_description_contents div").text.encode("utf-8")
    except:
        desc = "No description."

    try:
        cat = driver.find_element_by_css_selector("#location").text.encode("utf-8")    
    except:
        cat = "No category."   
    # try:
        # tier1qty = driver.find_element_by_css_selector("#right div.detail div:nth-child(2) div table tbody tr:nth-child(1) td:nth-child(1)").text.encode("utf-8")
    # except:
        # tier1qty = "No tier 1 qty."
        
    # try:
        # tier2qty = driver.find_element_by_css_selector("#right div.detail div:nth-child(2) div table tbody tr:nth-child(2) td:nth-child(1)").text.encode("utf-8")
    # except:
        # tier2qty = "No tier 2 qty."
        
    # try:
        # tier3qty = driver.find_element_by_css_selector("#right div.detail div:nth-child(2) div table tbody tr:nth-child(3) td:nth-child(1)").text.encode("utf-8")
    # except:
        # tier3qty = "No tier 3 qty."
        
    # try:
        # tier1price = driver.find_element_by_css_selector("#right div.detail div:nth-child(2) div table tbody tr:nth-child(1) td:nth-child(2)").text.encode("utf-8")
    # except:
        # tier1price = "No tier 1 price."
        
    # try:
        # tier2price = driver.find_element_by_css_selector("#right div.detail div:nth-child(2) div table tbody tr:nth-child(2) td:nth-child(2)").text.encode("utf-8")
    # except:
        # tier2price = "No tier 2 price."
        
    # try:
        # tier3price = driver.find_element_by_css_selector("#right div.detail div:nth-child(2) div table tbody tr:nth-child(3) td:nth-child(2)").text.encode("utf-8")
    # except:
        # tier3price = "No tier 3 price."
    
    try:
        dm = desc.split()
        dim = dm[len(dm)+1]
    except:
        dim = "No dimension available."

    try:
        images = []
        image = driver.find_elements_by_css_selector("#product_addtocart_form div.product-img-box div ul li a")
        for i in image:
            img = i.get_attribute("href")
            print img
            images.append(img)
    except:
        images = "No pics."

        

    ls = []
    
    ls.append(name)
    
    ls.append(skus)

    # ls.append(cat)
    
    ls.append(desc)
    
    # ls.append(tier1qty)
    
    # ls.append(tier1price)
    
    # ls.append(tier2qty)
    
    # ls.append(tier2price)
    
    # ls.append(tier3qty)
    
    # ls.append(tier3price)

    ls.append(images)
    
    print ls
    
    out.append(ls)


    
    
####################################################################################################################################################################################################################################
    
                
br = init_driver()
#init_login(br,uname,passw)
time.sleep(1)
br.get(url)
print "Waiting for homepage to load..."
time.sleep(1)


items = []
table = []
cats = []

with open("./csv/infile/debry_infile.csv","rb") as infile:
    for i in infile:
        print "Searching for item " + str(i)
        br.find_element_by_name("s").clear()
        br.find_element_by_name("s").send_keys(i)
        time.sleep(1)
        try:
            item = br.find_elements_by_css_selector("h2.product-name a")
            for i in item:
                itm = i.get_attribute("href")
                print itm
                items.append(itm)
        except:
            print "No item found. Searching for next key..."
            
print "All items now has been saved. Getting attributes for each..."            

ulist = list(set(items))
for i in ulist:
    print "Navigating to " + str(i)
    br.get(i)
    time.sleep(1)
    get_info(br,i,table)
        




print "***Job Done***"
              
        
        
outfile = open("./csv/outfile/debry_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)