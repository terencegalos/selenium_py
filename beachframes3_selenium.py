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

login = "https://www.kkinteriors.com/login"
uname = "service@waresitat.com"
passw = "wolfville"
url = "http://www.beachframes.com/"

    
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

br = init_driver()

br.get(url)
time.sleep(1)

table = []
items = []
# with open("./csv/infile/beachframes.csv","rb") as infile:
    # for i in infile:
        # print "\nSearching for item: " +str(i) + "\n"
        # time.sleep(1)
        # WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "search"))).clear()
        # br.find_element_by_id("search").send_keys(i)
        # time.sleep(1)
        # WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#search_mini_form button"))).click()
        # time.sleep(2)
        
 
        # try:
            # WebDriverWait(br, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2.product-name a")))
            # br.find_element_by_css_selector("section section.main-container.col2-left-layout div div.row div.col-lg-9.col-sm-9.col-xs-12 div div.category-products.pt-default div.toolbar-top div div.sorter div.limiter select option:nth-child(3)").click()
            # time.sleep(1)
            # item = br.find_elements_by_css_selector("h2.product-name a")
            # for i in item:
                # itm = i.get_attribute("href")
                # print itm
                # items.append(itm)
        # except:
            # print "No item found."
            
# item_links = list(set(items))            

# outfile1 = open("./csv/outfile/beachframes_links.csv","wb")
# writer1 = csv.writer(outfile1)
# writer1.writerow(item_links)             
        

with open("./csv/infile/beachframes_links.csv","rb") as infile:        
    for i in infile:
        print "Navigating to item: " + i + "\n"
        while True:
            try:
                ls = []
                br.get(i)                
                time.sleep(3)
                
                name = WebDriverWait(br, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-name h1")))
                try:
                    sku = name.text.split("(")
                    sku = sku[1]
                except:
                    sku = "None"
                
                time.sleep(3)
                
                image = WebDriverWait(br, 2).until(EC.presence_of_element_located((By.ID, "image")))
                img = image.get_attribute("src")
                
                ls.append(name.text.encode("utf-8"))
                ls.append(sku)
                ls.append(img)
                table.append(ls)
                print ls
            except:
                br.refresh()
                continue
                print "Some error occured. Retrying.."
            else:
                break
        # except:
            # print "Some error occured."
        
        
outfile = open("./csv/outfile/beachframes1.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)        