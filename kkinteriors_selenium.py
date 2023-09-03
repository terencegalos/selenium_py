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
import image_download as imgdl


login = "https://www.kkinteriors.com/login"
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
        
def get_info(driver,out):
    ls = []
    time.sleep(3)
    sku = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,"productnumbertext")))
    try:
		image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,"productimage"))).get_attribute("src")
		if ".jpg" not in image.split("/")[-1:][0]:
			print "Broken image link detected."
			return
    except:
        print "No image found."
        image = "None."
    ls.append(sku.text.encode("utf-8"))
    try:
        cat = "|".join([c.text for c in driver.find_elements_by_css_selector("#product-detail-spreads h1")])
    except:
        cat = "No category found."
    ls.append(cat)
    ls.append(image)
    out.append(ls)
    print ls

br = init_driver()
init_login(br,uname,passw)
table = []


with open("./csv/infile/kkitems.csv","rb") as infile:
    for i in infile:
        ls = []
        print "Searching for item: " + str(i)
        while True:
            try:
                br.find_element_by_id("search_box").send_keys(i)
                time.sleep(2)
                break
            except:
                br.refresh()
                time.sleep(1)
                continue
        
        try:
            WebDriverWait(br,10).until(EC.visibility_of_element_located((By.CLASS_NAME,"productimage"))).click()
            get_info(br,table)
        except:
            print "No item found."
		#download pics to desired directory
		# name = image.get_attribute("src").split("/")[-1:]
		# path = r'E:\rick stuart images\k&k\New folder (11)' + "\\" + str(name[0].strip())
		# print path
		# try:
			# urllib.urlretrieve(image.get_attribute("src"),path)
		# except:
			# pass

print "***Job Done***"        
        
outfile = open("./csv/outfile/kk_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

#download images
imgdl.get_images("kk",[i[2] for i in table])

br.close()