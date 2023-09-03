from selenium import webdriver
import time
import urllib2
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from urllib import urlopen
import urllib
import csv

url = "https://www.cowgirlchocolates.com/shop.shtml"
cats = ["https://www.cowgirlchocolates.com/shop_chocolates.shtml","https://www.cowgirlchocolates.com/shop_chocolate_bars.shtml","https://www.cowgirlchocolates.com/shop_caramels.shtml","https://www.cowgirlchocolates.com/shop_cocoa_treats.shtml","https://www.cowgirlchocolates.com/shop_colts_fillies.shtml","https://www.cowgirlchocolates.com/shop_gifts_occasions.shtml","https://www.cowgirlchocolates.com/shop_gear.shtml"]

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    

#initialize and open browser
br = init_driver()

category = []
for cat in cats:
    br.get(cat)
    links = br.find_elements_by_css_selector(".body a")
    for link in links:        
        lnk = link.get_attribute("href")
        category.append(lnk)
        print lnk
       
table = []    
for i in category:
    ls = []
    print "Navigating to: " + i

    br.get(i)
    time.sleep(1)
    try:
        name = br.find_element_by_class_name("shophead")
        sku = br.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/font[2]/b[2]/span[2]")
        desc = br.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/font[3]")
        qty = br.find_element_by_name("Quantity")
        price = br.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[3]/table/tbody/tr[1]/td[1]/font[2]/b[3]/span[2]")
        choices = br.find_elements_by_tag_name("option")
        image = br.find_element_by_xpath("/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/img")
        ls.append(name.text.encode("utf-8"))
        ls.append(sku.text.encode("utf-8"))
        ls.append(desc.text.encode("utf-8"))
        ls.append(qty.get_attribute("value").encode("utf-8"))
        ls.append(price.text.encode("utf-8"))
        ls.append([choice.text.encode("utf-8") for choice in choices])
        ls.append(image.get_attribute("src"))
        table.append(ls)
        print ls
    except:
        print "An error occurred."
    
outfile = open("./csv/outfile/cowgirlchocolates_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)    