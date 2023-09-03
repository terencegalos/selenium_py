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
        
        print ("Login Success.")
    except:
        print "Login failed."
        
#initialize and open browser
br = init_driver()
init_login(br,uname,pw)
time.sleep(5)


items = []
with open("./csv/infile/audreysku.csv","rb") as infile:
    for i in infile:
        print i
        br.find_element_by_id("ctl00_myheader_ctrlSearch_SearchText").send_keys(i)
        time.sleep(2)
        itms = br.find_elements_by_css_selector("div.info a")
        for i in itms:
            items.append(i.get_attribute("href"))

table = []            
for item in items:
    ls = []
    while True:
        try:
            br.get(item)
            time.sleep(3)
            sku = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sku")))
            cat = br.find_element_by_id("breadcrumb")
            image = br.find_element_by_css_selector("div.ProductDiv img")
            ls.append(sku.text.encode("utf-8"))
            ls.append(cat.text.encode("utf-8"))
            ls.append(image.get_attribute("src"))
            table.append(ls)
            print ls
        except:
            continue
        else:
            break
    
    

outfile = open('./csv/outfile/audreysimage.csv','wb')
writer = csv.writer(outfile)
writer.writerows(table)
