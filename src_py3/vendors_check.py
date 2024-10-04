import time
import csv
import os, sys, shutil
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import helper.webdriver_config as driver
#id = sys.argv[1]

br = driver.init_driver()
time.sleep(1)

username = input("Enter login credentials to start with username:")
password = input("Enter password:")
br.get("https://"+username+":"+password+"@www.waresitat.com/adminpage/index.cfm") #navigate with site credentials
time.sleep(1)

br.get("https://www.waresitat.com/adminpage/vendors/index.cfm")
time.sleep(1)

vendors = br.find_elements(By.CSS_SELECTOR,"#providers_list > tbody > tr")

table = []
for v in vendors:
    name = v.find_element(By.CSS_SELECTOR,"td:nth-child(2) > span").text.strip()
    mail = v.find_element(By.CSS_SELECTOR,"td:nth-child(3) > a").text.strip()
    date = v.find_element(By.CSS_SELECTOR,"td:nth-child(4)").text.strip()
    print([name,mail,date])
    table.append([name,mail,date]) if len(date) > 0 else ""
    
    
outfile = open("./csv/outfile/vendor_stat.csv","w")
writer = csv.writer(outfile)
writer.writerows(table)
outfile.close()


print("Vendors checked.")
br.close()
                    
                    
                    

