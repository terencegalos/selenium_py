from selenium import webdriver
import time
import urllib
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from urllib2 import urlopen
import csv

pages = ["http://www.yourheartsdelight.com/c-152-autumn-welcome.aspx?pagesize=96","http://www.yourheartsdelight.com/c-401-fall-fun.aspx","http://www.yourheartsdelight.com/c-1274-pumpkin-patch-pals.aspx","http://www.yourheartsdelight.com/c-1355-branches.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1378-candle-rings.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1357-collections.aspx","http://www.yourheartsdelight.com/c-1386-premade.aspx","http://www.yourheartsdelight.com/c-1349-picks.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1367-garlands.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1348-wreaths.aspx?pagesize=96","http://www.yourheartsdelight.com/c-593-boxes.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1272-burlap-ornaments.aspx?pagesize=96","http://www.yourheartsdelight.com/c-598-candles-lights-accessories.aspx?pagesize=96","http://www.yourheartsdelight.com/c-180-containers.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1165-decorative-plates-bowls.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1165-decorative-plates-bowls.aspx?pagesize=96","http://www.yourheartsdelight.com/c-363-dolls.aspx?pagesize=96","http://www.yourheartsdelight.com/c-637-fall-accents.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1164-frames-wall-decor.aspx?pagesize=96","http://www.yourheartsdelight.com/c-600-home-fragrance.aspx","http://www.yourheartsdelight.com/c-402-magnets.aspx","http://www.yourheartsdelight.com/c-362-ornaments.aspx","http://www.yourheartsdelight.com/c-1192-outdoor-decor.aspx","http://www.yourheartsdelight.com/c-400-pins.aspx","http://www.yourheartsdelight.com/c-82-pumpkins.aspx?pagesize=96","http://www.yourheartsdelight.com/c-616-runners-mats.aspx?pagesize=96","http://www.yourheartsdelight.com/c-364-scarecrows.aspx?pagesize=96","http://www.yourheartsdelight.com/c-708-tableware.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1177-thanksgiving.aspx?pagesize=96","http://www.yourheartsdelight.com/c-804-twigs.aspx?pagesize=96"]
uname = "service@waresitat.com"
pw = "wolfville"
url = "https://www.yourheartsdelight.com/Wholesale_signin.aspx?"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]
    
def init_login(driver,un,passw):    
    driver.get(url)
    try:
        print "Logging in..."
        WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "ctl00_PageContent_EMail"))).send_keys(un)
        WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "ctl00_PageContent_txtPassword"))).send_keys(pw)
        btn = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "ctl00_PageContent_LoginButton")))
        btn.click()
        print "Login Success."
    except:
        print "Login failed."
        
        
br = init_driver()
init_login(br,uname,pw)
links = []
with open("./csv/infile/audreysku.csv","rb") as infile:
    for i in infile:
        print i
        time.sleep(2)
        WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "ctl00_myheader_ctrlSearch_SearchText"))).clear()
        WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, "ctl00_myheader_ctrlSearch_SearchText"))).send_keys(i)
        time.sleep(1)
        try:
            lnk = WebDriverWait(br, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.info a")))
            link = lnk.get_attribute("href")
            links.append(link)
            print link
        except:
            print "Item not found."

table = []         
for link in links:
    ls = []
    print "Navigating to: " + str(link)
    br.get(link)
    time.sleep(1)
    sku = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sku")))
    cat = br.find_element_by_class_name("SectionTitleText")
    image = br.find_element_by_css_selector("div.ProductDiv img")
    ls.append(sku.text.encode("utf-8"))
    ls.append(cat.text.encode("utf-8"))
    ls.append(image.get_attribute("src"))
    print ls
    table.append(ls)
    
outfile = open("./csv/outfile/audreysitemsresults.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
    
outfile1 = open("./csv/outfile/audreyslinks.csv","wb")
writer1 = csv.writer(outfile1)
writer1.writerow(links)