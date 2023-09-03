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



url = "http://www.packagingsource.com/"
uname = "rick@waresitat.com"
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    br.get("http://barncandles.americommerce.com/")
    time.sleep(1)
    btn = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#utilnav ul li:nth-child(2) font b a")))
    btn.click()
    time.sleep(1)
    print "Logging in."
   
    driver.find_element_by_name("txtEmailAddress").send_keys(un)
    driver.find_element_by_name("txtPassword").send_keys(pw)
    driver.find_element_by_name("btnSignIn").click()
    time.sleep(5)
    print "Logged in."


        
br = init_driver()
br.get(url)
time.sleep(4)
print "Waiting for homepage to load..."
items = []
table = []

with open("./csv/outfile/thepackagingsource.csv","rb") as infile:
    for i in infile:
        print "Navigating to: " + str(i)
        br.get(i)
        time.sleep(1)
        try:
            br.find_element_by_css_selector("#ddShowByPageSize option:nth-child(5)").click()
            time.sleep(2)
            item = br.find_elements_by_css_selector("div.no-m-b a")
            for i in item:
                itm = i.get_attribute("href")
                items.append(itm)
                print itm
        except:
            print "More items found. Navigating each for more items.."
            item = br.find_elements_by_css_selector("div.CategoryCategoryThumbnail a")
            for i in item:
                itm = i.get_attribute("href")
                items.append(itm)
                print itm
                
                


print "***Job Done***"        
        
outfile = open("./csv/outfile/thepackagingsource_items.csv","wb")
writer = csv.writer(outfile)
writer.writerow(items)