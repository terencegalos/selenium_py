import time
import csv
import os, sys, shutil
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import helper.destination as destination
from helper.gateway import Vendor

import helper.webdriver_config as driver
id = sys.argv[1]

br = driver.init_driver()
time.sleep(1)

username = input("Enter login credentials to start with username:")
password = input("Enter password:")
br.get("https://{}:{}@www.waresitat.com/adminpage/index.cfm".format(username,password)) #navigate with site credentials
time.sleep(1)


br.get("https://www.waresitat.com/adminpage/vendors/index.cfm")
time.sleep(1)

vendor = Vendor(id)
# print(vendor)

vendors = [link.get_attribute("href") for link in br.find_elements(By.CSS_SELECTOR,"#providers_list > tbody > tr > td:nth-child(8) a")]
# print("\n".join(vendors))

link = ""

for i in vendors:
    # print(i)
    mid = i.split("ID=")[1]
    if str(vendor.code) in mid:
        print("link found.")
        print(i)
        link = i
        

br.get(link)
time.sleep(1)

			
print(vendor.name)
br.find_element(By.NAME,"csv_file").send_keys(destination.dir+vendor.filename) #get input file
time.sleep(1)

br.find_element(By.NAME,"action").click() #submit
time.sleep(1)

WebDriverWait(br,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[value=\"Save List\"]"))).click() # save


print("Vendor uploaded.")

sys.exit()                    
                    
                    

