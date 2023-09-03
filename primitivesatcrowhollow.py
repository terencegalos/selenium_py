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

login = "http://www.wtcollectionshowroom.com/cgi-wtcollectionshowroom/sb/order.cgi?func=2&storeid=*1209f4a48ae200708d5090&html_reg=html"
url = "http://www.primitivesatcrowhollow.com/store/Default.asp"
uname = "service@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):    
    driver.get(login)
    time.sleep(3)
    try:
        print "Logging in..."
        driver.find_element_by_name('email1').send_keys(un)
        driver.find_element_by_name('text1').send_keys(pw)
        driver.find_element_by_class_name("button166").click()
        print "Login Success."
        time.sleep(10)
    except:
        print "Login failed."
            

#initialize and open browser
br = init_driver()
br.get(url)
time.sleep(1)


items = []
with open("./csv/infile/primitivesatcrowhollow.csv","rb") as infile:
    for i in infile:
        print "Searching for item " + str(i)
        WebDriverWait(br, 5).until(EC.presence_of_element_located((By.NAME, "qrySearch"))).clear()
        try:
            WebDriverWait(br, 5).until(EC.presence_of_element_located((By.NAME, "qrySearch"))).send_keys(str(i.encode("utf-8")))
        except:
            continue
            print "Some error while searching item " + str(i)
        time.sleep(1)
        try:
            item = br.find_element_by_css_selector("body div center table tbody tr:nth-child(2) td:nth-child(2) div table tbody tr td p font table:nth-child(1) tbody tr td table:nth-child(4) tbody tr td table tbody tr:nth-child(2) td a")
            items.append(item.get_attribute("href"))
            print item.get_attribute("href")
        except:
            print "No item found/Some error occured."

table = []

outfile1 = open("./csv/outfile/primitivesatcrowhollow_results.csv","wb")
writer1 = csv.writer(outfile1)
writer1.writerow(items)

for item in items:
    ls = []
    br.get(item)
    time.sleep(1)
    name = WebDriverWait(br, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body div center table tbody tr:nth-child(2) td:nth-child(2) div table tbody tr td p font table:nth-child(2) tbody tr td div:nth-child(5) center table tbody tr:nth-child(1) td:nth-child(2) p:nth-child(1) font")))
    print name.text
    ls.append(name.text)
    desc = br.find_element_by_css_selector("body div center table tbody tr:nth-child(2) td:nth-child(2) div table tbody tr td p font table:nth-child(2) tbody tr td div:nth-child(5) center table tbody tr:nth-child(1) td:nth-child(2) font:nth-child(4)")
    print desc.text
    ls.append(desc.text)
    outimage = br.find_element_by_css_selector("body div center table tbody tr:nth-child(2) td:nth-child(2) div table tbody tr td p font table:nth-child(2) tbody tr td div:nth-child(5) center table tbody tr:nth-child(1) td:nth-child(1) p a")
    outimage.click()
    time.sleep(1)
    image = []
    for handle in br.window_handles:
        br.switch_to_window(handle)
        img = br.find_element_by_tag_name("img")
        print [img.get_attribute("src")]
        image.append(img.get_attribute("src"))
        br.switch_to_default_content()
    
    for i in image:
        ls.append(i)
    
    print ls
    table.append(ls)
    
outfile = open("./csv/outfile/primitivesatcrowhollow_results_final.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)


print "***Job Done!***"