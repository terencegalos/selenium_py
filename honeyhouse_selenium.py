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
from selenium.webdriver.common.action_chains import ActionChains



url = "http://www.honeyhousenaturals.com/16/home.htm"
uname = "waresitat"
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    br.get(url)
    time.sleep(1)
    btn = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#container table tbody tr:nth-child(1) td div table tbody tr td div.utilitynav a:nth-child(2)")))
    btn.click()
    time.sleep(1)
    print "Logging in."
   
    name = WebDriverWait(driver,60).until(EC.visibility_of_element_located((By.NAME,"UserName")))
    name.send_keys(un)
    driver.find_element_by_name("Password").send_keys(pw)
    driver.find_element_by_id("LogonSave").click()
    time.sleep(1)
    print "Logged in."


        
br = init_driver()
br.get(url)
init_login(br,uname,passw)
time.sleep(15)




items = []
table = []

    


with open("./csv/infile/honeyhouse.csv","rb") as infile:
    for i in infile:
        ls = []
        br.find_element_by_id("SearchText").clear()
        br.find_element_by_id("SearchText").send_keys(i)
        print "Searching for " + str(i)
        time.sleep(1)
        
        try:
            item = br.find_elements_by_css_selector("div.quickorderproductname a")
            for itm in item:
                link = itm.get_attribute("href")
                ls = []
                br.get(link)
                time.sleep(1)
                name = br.find_element_by_css_selector("div.COMProductName").text.encode("utf-8")
                sku = br.find_element_by_id("CurrentItemDiv").text.encode("utf-8")
                image = br.find_element_by_id("COMProdImage").get_attribute("src")
    
                ls.append(i)
                ls.append(name)
                ls.append(sku)
                ls.append(image)
                
                print ls
                table.append(ls)
        except:
            print "No item found. Searching next item..."
            
            
print "***Job Done***"        
        
outfile = open("./csv/outfile/honeyhouse_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)