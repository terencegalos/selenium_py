from selenium import webdriver
import time
import urllib2
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from urllib import urlopen
import urllib
import csv

uname = "rick@waresitat.com"
passw = "wolfville"
login = "http://www.oakstreetwholesale.com/store/login.html"

table = []
def init_driver():
    path = "./chrome_drive/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):    
    driver.get(login)
    time.sleep(3)
# try:
    print "Logging in..."
    driver.find_element_by_id('login-username').send_keys(un)
    driver.find_element_by_id('login-password').send_keys(pw)
    driver.find_element_by_name("submit").click()
    print "Login Success."
    time.sleep(5)
# except:
    # print "Login failed."    
    
def init_scrape(url):
    ls = []
    br.get(url)
    time.sleep(1)
    name = WebDriverWait(br, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "title-bg")))
    # name = br.find_element_by_class_name('title-bg')
    sku = br.find_element_by_id('prod-code')
    img = br.find_element_by_class_name('img-size')
    cat = br.find_element_by_xpath("//*[@id=\"breadcrumb\"]/ul")
    desc = br.find_element_by_id('product_description')
    print desc.text
    
    priceqty = []
    try:
        br.find_element_by_partial_link_text("Quantity Discounts").click()
        time.sleep(3)
        pricebreaks = br.find_elements_by_tag_name("tr")       
        
        for pricebreak in pricebreaks[1:]:
            qtyprice = pricebreak.text.split(" ")
            for i in qtyprice:
                print i
                priceqty.append(i)                
    except:
        "No price break available."
        priceqty.append([])
        
    ls.append(name.text.encode("utf-8"))
    ls.append(sku.text.encode("utf-8"))
    ls.append(cat.text.encode("utf-8"))
    ls.append(desc.text.encode("utf-8"))
    ls.append(priceqty)
    ls.append(img.get_attribute("src"))
    print "Image: "+ img.get_attribute("src")
    table.append(ls)
    print ls
    
br = init_driver()  
init_login(br,uname,passw)  
    
with open('./csv/infile/oakstreetsearchresult2.csv','rb') as infile:
    for i in csv.reader(infile):
        for item in i:
            print "Scraping info for: " + str(item)           
            print item
            try:
                init_scrape(item)
            except:
                print "Some error occured."

            
   
outfile = open('./csv/outfile/oakstreetitemsresult.csv','wb')
writer = csv.writer(outfile)
writer.writerows(table)
        