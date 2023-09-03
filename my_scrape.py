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
url = "https://www.acheerfulgiver.com/"
sales = "https://adamsandco.net/category.php?category=30"
farm = "https://www.acheerfulgiver.com/candles/farm-fresh.html"
mylink = "http://www.jorpetz.com/galleries/adultery-scandal-ni-yvette-karen-1264.html"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):
    driver.get("https://www.acheerfulgiver.com/customer/account/login/")
    time.sleep(1)
    print "Logging in..."
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"email"))).send_keys(un)
    driver.find_element_by_id('pass').send_keys(pw)
    driver.find_element_by_css_selector("#send2 span span").click()
    print "Login Success."
    time.sleep(10)
    # except:
        # print "Login failed."
		

            

#initialize and open browser
br = init_driver()
time.sleep(3)


items = []
table = []

br.get(mylink)
time.sleep(1)

links = [it.get_attribute("href") for it in br.find_elements_by_css_selector("#galleryImages > a")]

for link in links:
	br.get(link)
	time.sleep(1)
	pic = br.find_element_by_css_selector("#singleImage > a > img").get_attribute("src")
	print pic
	table.append(pic)
	

outfile = open("./csv/outfile/myresult.csv","wb")
writer = csv.writer(outfile)
writer.writerow(table)                        
