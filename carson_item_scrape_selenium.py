from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv

uname = "kwares"
pw = "Williams2"
URL = "https://www.carsonhomeaccents.com/security_logon.asp?autopage=%2Fdefault%2Easp"
items = []

def init_driver():
    path = "./chrome_drive/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):    
    driver.get(URL)
    try:
        print "Logging in..."
        driver.find_element_by_id('logonUsername').send_keys(un)
        driver.find_element_by_id('logonPassword').send_keys(pw)
        driver.find_element_by_name('B1').click()

        print ("Login Success.")
    except:
        print "Login failed."

#initialize and open browser
br = init_driver()
init_login(br,uname,pw)

table = []
with open('./csv/infile/carsonitemlinks.csv','rb') as infile:

    for item in infile:
        ls = []
        print "Navigating to item: " + str(item)
        br.get(item)
        time.sleep(1)
        # sku = br.find_element_by_id("detail_info_sku")
        sku = WebDriverWait(br, 20).until(EC.presence_of_element_located((By.ID, "detail_info_sku")))
        desc = br.find_element_by_class_name("detail_desc_content")
        image = br.find_element_by_id("detail_enlarge")
        ls.append(sku.text.encode("utf-8"))
        ls.append(desc.text.encode("utf-8"))
        ls.append(image.get_attribute("href"))
        table.append(ls)
        print "**Attributes scraped."
        print ls

    
outfile1 = open('./csv/outfile/carsonitemlinks.csv','wb')
writer1 = csv.writer(outfile1)
writer1.writerow(items)

 
outfile = open('./csv/outfile/carsonresults.csv','wb')
writer = csv.writer(outfile)
writer.writerows(table)

print "Job done."