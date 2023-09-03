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

br = driver.init_driver()
time.sleep(1)

# br.get("https://wares:w@r3s@www.waresitat.com/adminpage/index.cfm") #navigate with site credentials
def login():
    br.get("https://www.waresitat.com/index.cfm")
    br.find_element_by_name("login_username").send_keys("canada2")
    br.find_element_by_name("password").send_keys("2")
    br.find_element_by_name("password").send_keys(Keys.ENTER)
    time.sleep(1)


url = "https://www.waresitat.com/vendor_detail.cfm?VendorID="
ismissing = "/pics/shared/image_not_available.gif"

select = "div.outerdivcatimgbox > div > a > img"

login()

withmissing = []

with open("./csv/outfile/vendor_ids.csv","rb") as infile:
    for line in infile:
        vendor = csv.reader(infile)
        for line in vendor:
            # try:
            print "Vendor:"+line[0]
            br.get(url+line[0])
            time.sleep(1)
            cats = [image.get_attribute("src") for image in br.find_elements_by_css_selector(select)]
            for cat in cats:
                if ismissing in cat:
                    print "Missing image detected."
                    withmissing.append(line[0])
            print "Images OK."

            # except:
            #     print "Skipping inactive vendor"
            