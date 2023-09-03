from selenium import webdriver
import time
import urllib
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv


uname = "service@waresitat.com"
passw = "wolfville"
login = "https://www.hcbyraghu.com/index.php?main_page=login"
url = "http://www.hcbyraghu.com/"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    driver.get(url)
    driver.find_element_by_css_selector("#logoWrapper div:nth-child(2) table tbody tr:nth-child(2) td:nth-child(1) a:nth-child(3)").click()
    time.sleep(1)
    print "Logging in."
    # try:
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID, "login-email-address"))).send_keys(un)
    driver.find_element_by_id("login-password").send_keys(pw)
    driver.find_element_by_css_selector("#loginForm div.buttonRow.forward input[type=\"image\"]").click()
    time.sleep(5)
    print "Logged in."
    # except:
        # print "Log in failed."
        # driver.close()    
 

br = init_driver()
init_login(br,uname,passw) 
time.sleep(3)

table = []

with open("./csv/infile/raghu.csv","rb") as infile:
    for i in infile:
        
        try:
            print "Searching for item: " + i
            br.find_element_by_id("searchboxinput").clear()
            br.find_element_by_id("searchboxinput").send_keys(str(i))
            time.sleep(1)
            
             
            items = WebDriverWait(br, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.itemTitle a")))
            for i in items:
                ls = []
                br.get(i.get_attribute("href"))
                time.sleep(1)
                sku = br.find_element_by_css_selector("#productDetailsList li")
                cat = br.find_element_by_css_selector("#productListHeading a")
                desc = br.find_element_by_css_selector("#productDescription")
                image = WebDriverWait(br, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#productMainImage a img")))                  
                
                ls.append(sku.text.split()[1])
                ls.append(cat.text.encode("utf-8"))
                ls.append(desc.text.encode("utf-8"))
                ls.append(image.get_attribute("src"))

                    
                print ls
                table.append(ls)
            
        except: 
            print "No item found. Getting next item..."

outfile = open("./csv/outfile/raghu_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)        