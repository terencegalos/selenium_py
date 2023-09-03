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


prodlist = "http://www.monahanpapers.com/go/itemlist.php"
url = "http://www.monahanpapers.com/"
uname = "rick@waresitat.com"
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    btn = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#TopMenu ul li:nth-child(4) div a:nth-child(1)")))
    btn.click()
    time.sleep(1)
    print "Logging in."
   
    driver.find_element_by_id("login_email").send_keys(un)
    driver.find_element_by_id("login_pass").send_keys(pw)
    driver.find_element_by_id("LoginButton").click()
    time.sleep(5)
    print "Logged in."


        
br = init_driver()
br.get(url)
time.sleep(3)
# btn = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ctl37_rpLinkList_ctl00_dvHorizontalNavItem a")))
# btn.click()
time.sleep(2)



items = []
table = []


# br.get(prodlist)
# WebDriverWait(br,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body table tbody tr:nth-child(2) td:nth-child(2) table tbody tr td div:nth-child(2) a")))
# item = br.find_elements_by_css_selector("body table tbody tr:nth-child(2) td:nth-child(2) table tbody tr td div:nth-child(2) a")
# for i in item:
    # items.append(i.get_attribute("href"))
    # print i.get_attribute("href")
                                                                              
    

with open("./csv/infile/monahan.csv","rb") as infile:

    for i in infile:
        ls = []
        br.get(i)
        print "Navigating to:\n" + str(i)
        time.sleep(1)

        name = WebDriverWait(br,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"td.productname")))
        cat = br.find_element_by_css_selector("body table tbody tr:nth-child(2) td:nth-child(2) table tbody tr td div:nth-child(1) p")
        try:
            desc = br.find_element_by_css_selector("body table tbody tr:nth-child(2) td:nth-child(2) table tbody tr td div:nth-child(2) form div table tbody tr:nth-child(3) td div:nth-child(2) span")
        except:
            desc = "None"
        # try:
            # options = br.find_element_by_css_selector("#options_table")
        # except:
            # print "No options available."
            # options = "None"

        # min = br.find_element_by_name("qtty")
        try:
            price = br.find_element_by_css_selector("span.pricereg")
        except:
            continue
            print "No price found. Skipping..."
        # try:
            # image = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body table tbody tr:nth-child(2) td:nth-child(2) table tbody tr td div:nth-child(2) form div table tbody tr:nth-child(1) td img")))
        # except:
            # print "No image found. Skipping.."
            # continue
            
        # try:
            # pricevary = br.find_elements_by_name("optval1")
        # except:
            # pricevary = br.find_element_by_css_selector("span.pricereg")
        ls.append(name.text.encode("utf-8"))
        ls.append(cat.text.encode("utf-8"))
        try:
            ls.append(desc.text.encode("utf-8"))
        except:
            ls.append(desc)
        # ls.append(min.get_attribute("value"))
       
        # try:  
            # var = []
            # for i in pricevary:
                # var.append(i.get_attribute("value"))
            # ls.append(var)
        # except:
            # ls.append(pricevary.text.encode("utf-8"))
        ls.append(price.text.encode("utf-8"))

        # ls.append(image.get_attribute("src"))
        table.append(ls)
        print ls


print "***Job Done***"        
        
outfile = open("./csv/outfile/monahanpapers2.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)