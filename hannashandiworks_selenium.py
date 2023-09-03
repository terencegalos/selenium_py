import webdriver_config
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

url = "http://www.hannashandiworks.com/"
sitemap = "https://shop.site-link.com/hannashandiworks/sitemap.asp"
uname = "rick@waresitat.com"
passw = "waresitat"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):
    driver.get("https://shop.site-link.com/hannashandiworks/login.asp")
    time.sleep(3)
    try:
        print "Logging in..."
        driver.find_element_by_name("regtxtemail").send_keys(un)
        driver.find_element_by_name("txtregpassword").send_keys(pw)
        driver.find_element_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(6) > tbody > tr:nth-child(3) > td.plaintext > center > table > tbody > tr:nth-child(5) > td > input[type=\"Image\"]").click()
        time.sleep(2)
        driver.find_element_by_css_selector("#Image1").click()
        time.sleep(1)
        print "Login Success."
    except Exception as e:
        print e
        print "Login failed."
       
       
def get_info(link,driver,out):
    print link
    driver.get(link)
    time.sleep(1)
    ls =[]
    name = driver.find_element_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(3) > tbody > tr > td").text.encode("utf-8")
    ls.append(name)
    sku = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(5) > tbody > tr > td:nth-child(3) > table > tbody > tr > td > table > tbody > tr:nth-child(1) > td")))
    ls.append(sku.text.split()[2])
    cat = "|".join([c.text for c in driver.find_elements_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(1) > tbody > tr > td > a")])
    ls.append(cat)
    try:
        #desc = driver.find_element_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(8) > tbody > tr:nth-child(2) > td > p").text.encode("utf-8")
        desc = "|".join([d.text.encode("utf-8") for d in driver.find_elements_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(9) > tbody > tr > td")])
    except:
        desc = "No desc."
    ls.append(desc)
    tier1 = driver.find_element_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(5) > tbody > tr > td:nth-child(3) > table > tbody > tr > td > table > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td > span").text.encode("utf-8")
    try:
        tier2 = driver.find_element_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(5) > tbody > tr > td:nth-child(3) > table > tbody > tr > td > table > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(2) > td > span").text.encode("utf-8")
    except:
        tier2 = "No tier2 no tier 2"
    ls.append(tier1.split()[1])
    ls.append(tier1.split()[3])
    ls.append(tier2.split()[1])
    ls.append(tier2.split()[3])
    try:
        image = driver.find_element_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(5) > tbody > tr > td:nth-child(1) > center > img").get_attribute("src")
        ls.append(image)
    except:
        image = "No image."
    out.append(ls)
    print ls
    
    
def get_item_links(driver,arr):
    # get items in first page
    print "Getting items for the first page.."
    item = [i.get_attribute("href") for i in driver.find_elements_by_css_selector("a.allpage")]
    arr.extend(item)
    print item
    time.sleep(2)
    # get the rest if pagination is available
    while True:
        # pagination
        pages = [x.get_attribute("href") for x in driver.find_elements_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(2) > tbody > tr:nth-child(1) > td > p.plaintextbold > a")]
        print "Length of pages are:"
        print len(pages)
        try:
            print driver.find_elements_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(2) > tbody > tr:nth-child(1) > td > p.plaintextbold > a")[-1].text
        except:
            print "Sole page detected. Getting items..."
            time.sleep(1)
            print [i.get_attribute("href") for i in driver.find_elements_by_css_selector("table > tbody > tr > td > a.allpage")]
            arr.extend([i.get_attribute("href") for i in driver.find_elements_by_css_selector("table > tbody > tr > td > a.allpage")])
            break
        time.sleep(5)
        print "Showing first page.."
        print pages
        for x in range(len(pages)):
            print x
            driver.get(pages[x])
            print "Next page.."
            time.sleep(1)
            it = [i.get_attribute("href") for i in driver.find_elements_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(6) > tbody > tr > td > table > tbody > tr > td > a")]
            print it
            arr.extend(it)
        if driver.find_elements_by_css_selector("td > p.plaintextbold > a")[-1].text != " More":
            print "Page exhausted."
            break
    

#initialize and open browser
br = webdriver_config.init_driver()
time.sleep(1)
init_login(br,uname,passw)
time.sleep(1)
br.get(sitemap)
time.sleep(1)

table = []
items = []
exceptions = ["https://shop.site-link.com/hannashandiworks/departments.asp?dept=263","https://shop.site-link.com/hannashandiworks/departments.asp?dept=192","https://shop.site-link.com/hannashandiworks/departments.asp?dept=38","https://shop.site-link.com/hannashandiworks/departments.asp?dept=255","https://shop.site-link.com/hannashandiworks/departments.asp?dept=549","https://shop.site-link.com/hannashandiworks/departments.asp?dept=280","https://shop.site-link.com/hannashandiworks/departments.asp?dept=473","https://shop.site-link.com/hannashandiworks/departments.asp?dept=102","https://shop.site-link.com/hannashandiworks/departments.asp?dept=265","https://shop.site-link.com/hannashandiworks/departments.asp?dept=264","https://shop.site-link.com/hannashandiworks/departments.asp?dept=276"]

cats = [c.get_attribute("href") for c in br.find_elements_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(3) > tbody > tr > td > a")]

for x in range(len(cats)):
    if cats[x] not in exceptions:
        print "Navigating to " + cats[x]
        time.sleep(3)
        br.get(cats[x])
        time.sleep(1)
        get_item_links(br,items)
        
# br.find_element_by_css_selector("body > center > table:nth-child(2) > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(4) > table > tbody > tr > td:nth-child(2) > select > option:nth-child(2)").click()
# time.sleep(1)  
      
# with open("./csv/infile/noimg/Hannas_Handiworks.csv","rb") as infile:
    # for i in [i for i in infile][1:4]:
        # print "Searching for " + i
        # br.find_element_by_name("txtsearch").clear()
        # br.find_element_by_name("txtsearch").send_keys(i.split(",")[1])
        # time.sleep(1)
        # try:
            # item = br.find_element_by_css_selector("body > center > table:nth-child(3) > tbody > tr > td.pagenavbg > center > table:nth-child(5) > tbody > tr:nth-child(3) > td:nth-child(3) > table > tbody > tr:nth-child(1) > td > a").get_attribute("href")
            # print item
            # items.append(item)
        # except:
            # print "Item not found."
        
for lnk in set(items):
    while True:
        try:
            get_info(lnk,br,table)
            break
        except:
            br.refresh()
            time.sleep(3)
            continue
    
    
        
outfile = open("./csv/outfile/images/hannashandiworks_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)     
print "***Job Done!***"   