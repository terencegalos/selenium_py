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

login = "https://adamsandco.net/home.php"
url = "https://www.regalgift.com/customer/account/login/referer/aHR0cDovL3d3dy5yZWdhbGdpZnQuY29tL2Ntcy9pbmRleC9ub1JvdXRlLw,,/"
uname = "waresitat"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):    
    driver.get(url)
    time.sleep(1)
    print "Logging in..."
    # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"body table tbody tr:nth-child(2) td:nth-child(1) a img"))).click()
    # time.sleep(1)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,"login[username]"))).send_keys(un)
    driver.find_element_by_name('login[password]').send_keys(pw)
    driver.find_element_by_css_selector("#send2 > span > span").click()
    print "Login Success."
    time.sleep(6)
    # except:
        # print "Login failed."
            

#initialize and open browser
br = init_driver()
br.get(url)
#init_login(br,uname,passw)
time.sleep(1)

items = []
table = []

with open("./csv/infile/regalgift.csv","rb") as infile:
    for i in infile:
        print "\nSearching for item " + str(i)
        br.find_element_by_name("q").clear()
        br.find_element_by_name("q").send_keys(i)       
        time.sleep(1)

        
        item = br.find_elements_by_css_selector("a.popup.cboxElement")
        for i in item:
            ls = []
            items.append(i.get_attribute("href"))
            print i.get_attribute("href")

for i in items:
    ls = []
    br.get(i)
    time.sleep(1)
    sku = WebDriverWait(br,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"td.sku"))).text.encode("utf-8")
    dim = br.find_element_by_css_selector(".size").text.encode("utf-8")
    image = br.find_element_by_css_selector("#imgCell img").get_attribute("src")

    ls.append(sku)
    ls.append(dim)
    ls.append(image)
    table.append(ls)
    print ls
        # except:
            # print "No item found."
			
			
outfile = open("./csv/outfile/regalgift_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()