

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



login = "https://www.kkinteriors.com/login"
url = "http://www.swancreekcandle.com/"
uname = "service@waresitat.com"
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
    
def init_login(driver,un,pw):
    driver.get(login)
    print "Logging in."
    try:
        driver.find_element_by_id("Username").send_keys(un)
        driver.find_element_by_id("Password").send_keys(pw)
        driver.find_element_by_css_selector("input.button").click()
        time.sleep(5)
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
        

        
        
        
        
        
urls = ["http://www.swancreekcandle.com/nemisaja.html","http://www.swancreekcandle.com/nededr.html","http://www.swancreekcandle.com/jarcandles.html","http://www.swancreekcandle.com/potterycandles.html","http://www.swancreekcandle.com/candlewarmers.html","http://www.swancreekcandle.com/nefroisp1.html","http://www.swancreekcandle.com/tawaxme.html","http://www.swancreekcandle.com/goen.html",]        
        
br = init_driver()
br.get(url)
time.sleep(1)



items = []
table = []



for lnk in urls:
    br.get(lnk)
    time.sleep(4)
    
    if lnk == "http://www.swancreekcandle.com/jarcandles.html" or lnk == "http://www.swancreekcandle.com/potterycandles.html" or lnk == "http://www.swancreekcandle.com/candlewarmers.html":
        links = br.find_elements_by_css_selector("div.name a")
        print "\nGetting deeper for links..."
        print "Here the links to go to:"
        urls = []
        for link in links:
            print link.get_attribute("href")
            urls.append(link.get_attribute("href"))
            
        
        for url in urls:
            print "Navigating to:"
            print url
            br.get(url)           
            time.sleep(2)
            item = br.find_elements_by_css_selector("div.name a")
            for i in item:
                items.append(i.get_attribute("href"))
                print i.get_attribute("href")
    else:
        item = br.find_elements_by_css_selector("div.name a")
        for i in item:
            items.append(i.get_attribute("href"))
            print i.get_attribute("href")   
            
                   

                
for item in items:
    try:
        get_info(br,item,table)
    except:
        continue


        
                
        
outfile = open("./csv/outfile/swancreekcandle.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"        
   