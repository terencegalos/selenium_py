import time
import sys
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
vendors = [link.get_attribute("href") for link in br.find_elements(By.CSS_SELECTOR,"#providers_list > tbody > tr > td:nth-child(8) a")]

link = ""

# find matching vendor
for i in vendors:
    mid = int(i.split("ID=")[1])

    try:
        if vendor.code == mid:
            print("Match found.")
            print("Link" + i)
            link = i
    except AttributeError:
        print(f"Vendor id {mid} cannot be found.")

try:
    br.get(link)
    time.sleep(1)

    print(vendor.name)
    br.find_element(By.NAME, "csv_file").send_keys(destination.dir + vendor.filename)  # get input file
    time.sleep(1)

    br.find_element(By.NAME, "action").click()  # submit
    time.sleep(1)

    try:
        WebDriverWait(br, 120).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[value=\"Save List\"]"))
        ).click()  # save
    except TimeoutError:
        WebDriverWait(br, 120).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[value=\"Save List\"]"))
        ).click()  # save

    # Robust check for upload success
    try:
        # Wait for success confirmation - look for common success indicators
        WebDriverWait(br, 30).until(
            lambda driver: "successful" in driver.page_source.lower() or 
                          "uploaded" in driver.page_source.lower() or
                          "complete" in driver.page_source.lower()
        )
        print("Upload verified as successful.")
    except:
        print("Warning: Upload may have failed - no success confirmation found on page.")
        # Optionally, you could raise an exception here to stop the script
        # raise Exception("Upload verification failed")

    print("Vendor uploaded.")
except Exception as e:
    print(f"An error occurred during the upload process: {e}")
finally:
    inp = input("Close browser? ")
    if 'yes' in inp.lower():
        try:
            if br is not None:
                br.quit()
                print("Browser closed successfully.")
            br = None  # Prevent further use of the object
        except Exception as quit_error:
            print(f"Error while closing the browser: {quit_error}")
