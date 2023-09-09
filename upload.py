import time
import csv
import os, sys, shutil
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import destination
from gateway import Vendor

import webdriver_config as driver
id = sys.argv[1]

br = driver.init_driver()
time.sleep(1)

inp = input("Enter login credentials to start:")
br.get(inp) #navigate with site credentials
time.sleep(1)


br.get("https://www.waresitat.com/adminpage/vendors/index.cfm")
time.sleep(1)

vendor = Vendor(id)
vendors = [link.get_attribute("href") for link in br.find_elements_by_css_selector("#providers_list > tbody > tr > td:nth-child(8) a")]

link = ""

for i in vendors:
    print i.encode("utf-8")
    mid = i.split("ID=")[1]    
    if vendor.code == mid:
        link = i
			
br.get(link)
time.sleep(1)

			
print vendor.name
# print vendor.filename.decode("latin-1")
br.find_element_by_name("csv_file").send_keys(destination.dir+vendor.filename.encode("utf-8")) #get input file
time.sleep(1)

br.find_element_by_name("action").click() #submit
time.sleep(1)

WebDriverWait(br,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[value=\"Save List\"]"))).click() # save


print "Vendor uploaded."

sys.exit()                    
                    
                    

