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
import os
import sys


# os.chdir(r"E:\rick stuart images\k&k\New folder (11)")
# print os.getcwd()
# time.sleep(1)

login = "https://www.kkinteriors.com/login"
uname = "service@waresitat.com"
passw = "wolfville"
url = "http://viphomeandgarden.com/"

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
        
def get_info(driver,out):
	ls = []
	sku = driver.find_element_by_css_selector("#wrap > section:nth-child(2) > div > div > div > div:nth-child(4) > h4").text.encode("utf-8")
	desc = driver.find_element_by_css_selector("#wrap > section:nth-child(2) > div > div > div > div:nth-child(4)").text.encode("utf-8")
	image = driver.find_element_by_css_selector("#wrap > section:nth-child(2) > div > div > div > div:nth-child(3) > a").get_attribute("href")
	ls.append(sku)
	ls.append(desc)
	ls.append(image)
	out.append(ls)
	print ls

br = init_driver()
#init_login(br,uname,passw)
br.get(url)
time.sleep(1)

items = []
table = []


with open("./csv/infile/vipgarden.csv","rb") as infile:
    for i in infile:
        ls = []
        print "Searching for item: " + str(i)
        while True:
            try:
                br.find_element_by_css_selector("#menu > li.search").click()
                #time.sleep(1)
                br.find_element_by_name("id").send_keys(i)
                time.sleep(1)
                break
            except:
                br.refresh()
                time.sleep(1)
                continue
        
        try:
            item = br.find_element_by_css_selector("#wrap > section:nth-child(2) > div > div > div > div > div > div > div > div > div > h3 > a").get_attribute("href")
            print item
            items.append(item)
            time.sleep(1)
        except:
            print "No item found."
for item in items:
    print "Navigating to " + item
    br.get(item)
    time.sleep(1)
    try:
        get_info(br,table)
    except:
        print "Item not found."
    
		#download pics to desired directory
		# name = image.get_attribute("src").split("/")[-1:]
		# path = r'E:\rick stuart images\k&k\New folder (11)' + "\\" + str(name[0].strip())
		# print path
		# try:
			# urllib.urlretrieve(image.get_attribute("src"),path)
		# except:
			# pass

print "***Job Done***"        
        
outfile = open("./csv/outfile/vipgarden_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()