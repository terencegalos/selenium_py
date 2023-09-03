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

login = "http://www.wtcollectionshowroom.com/cgi-wtcollectionshowroom/sb/order.cgi?func=2&storeid=*1209f4a48ae200708d5090&html_reg=html"
url = "http://www.wtcollectionshowroom.com/store/viewproducts.html"
uname = "service@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):    
    driver.get(login)
    time.sleep(3)
    try:
        print "Logging in..."
        driver.find_element_by_name('email1').send_keys(un)
        driver.find_element_by_name('text1').send_keys(pw)
        driver.find_element_by_class_name("button166").click()
        print "Login Success."
        time.sleep(10)
    except:
        print "Login failed."
            

#initialize and open browser
br = init_driver()
init_login(br,uname,passw)
br.get(url)

table = []
with open("./csv/infile/wingtai_infile.csv","rb") as infile:
    for i in infile:
        try:
            ls = []
            time.sleep(1)
            br.find_element_by_name("search_field").clear()
            br.find_element_by_name("search_field").send_keys(i)
            time.sleep(1)
            name = br.find_element_by_css_selector("#bb-loopproducts > li > div > div > div").text.encode("utf-8")
            sku = br.find_element_by_css_selector("#bb-loopproducts > li > div > div > span").text.encode("utf-8")
            img = br.find_element_by_css_selector("#bb-loopproducts > li > div > span > img").get_attribute("src")
            cats = "|".join([(i.text.encode("utf-8")).strip() for i in br.find_elements_by_css_selector("#bb-loopproducts > li > a")])
            ls.append(name)
            ls.append(sku)
            ls.append(cats)
            ls.append(img)
            table.append(ls)
            print ls
        except NoSuchElementException:
            print "Item not found."
outfile = open("./csv/outfile/wingtai_ouput2.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)        