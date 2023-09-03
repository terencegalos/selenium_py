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

url = "https://olivias-heartland-wholesale.myshopify.com/"
uname = "kaye.williams@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_css_selector("#external_links > ul.hidden-xs.nav.navbar-nav.navbar-right > li:nth-child(2) > a > span > i").click()
    time.sleep(1)
    driver.find_element_by_css_selector("#external_links > ul.hidden-xs.nav.navbar-nav.navbar-right > li.dropdown-grid.no-open-arrow.open > div > div > div > div.login_frm > div > a:nth-child(1)").click()
    time.sleep(1)
    
    try:
        print "Logging in..."
        driver.find_element_by_name('customer[email]').send_keys(un)
        driver.find_element_by_name('customer[password]').send_keys(pw)
        driver.find_element_by_css_selector("#customer_login > div.row > div.col-sm-5.col-ms-6.col-xs-4 > p > input").click()
        print "Login Success."
        time.sleep(1)
    except:
        print "Login failed."
         
def get_info(driver,out):
    ls =[]

    name = driver.find_element_by_css_selector("#content > div > div.title.clearfix > h1").text.encode("utf-8")
    sku = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#addToCartForm > div > div.rte > p")))
    try:
        cat = "|".join([c.text for c in driver.find_elements_by_css_selector("#content > div > ol > li")])
    except:
        cat = "No cat."
    try:
        desc = "|".join([desc.text for desc in driver.find_elements_by_css_selector("#addToCartForm > div > div.rte > ul > li")])
    except:
        desc = "No dim."
    try:
        min = driver.find_element_by_css_selector("#quantity").get_attribute("value")
    except:
        min = "No min."
    try:
        price = driver.find_element_by_css_selector("#productPrice").text.encode("utf-8")
    except:
        price = "No price."
    try:
        image = driver.find_element_by_css_selector("#image-block > div > a > img:nth-child(1)").get_attribute("src")
    except:
        image = "No image."
    
    ls.append(name)
    ls.append(sku.text.split(": ")[1])
    ls.append(cat)
    ls.append(desc)
    try:
        ls.append(desc[1])
    except:
        ls.append("No dim.")
    ls.append(min)
    ls.append(price)
    ls.append(image)
    
    out.append(ls)
    print ls

#initialize and open browser
br = webdriver_config.init_driver()
init_login(br,uname,passw)

table = []
items = []
cats = []

cat = br.find_elements_by_css_selector("#external_links > ul.nav.navbar-nav.navbar-left.dropdown-onhover > li > ul > li > a")
for puss in cat:
    c = puss.get_attribute("href")
    print c+"\n"
    cats.append(c)
    
def get_items(driver,out):
    list = driver.find_elements_by_css_selector("#content > div > div > div.row > div > div > div.row.view-grid.animated.fadeInUp.animation-done > div > div > div.box_1 > form > div > a")
    for x in list:
        xt = x.get_attribute("href")
        print xt
        out.append(xt)
    flag = False
    print "\nItems found.\n"
    
    
# with open("./csv/infile/olivias.csv","rb") as infile:
    # for i in infile:
        # print "Searching for item " + i

        # time.sleep(1)
        # br.find_element_by_css_selector("#external_links > ul.hidden-xs.nav.navbar-nav.navbar-right > li:nth-child(3) > a > span > i").click()
        # time.sleep(1.5)
        # br.find_element_by_name("q").clear()
        # time.sleep(0.2)
        # br.find_element_by_name("q").send_keys(i.strip())
        # br.find_element_by_css_selector("#external_links > ul.hidden-xs.nav.navbar-nav.navbar-right > li.dropdown-grid.no-open-arrow.open > div > div > form > div > div > button > span").click()
        # time.sleep(1)

        # item = br.find_elements_by_css_selector("#content > div > div > div > div > div > div.desc > h5 > a")
        # for i in item:
            # hrf = i.get_attribute("href")
            # print hrf
            # items.append(hrf)

        
        
        
        
        
        
# more cats?
flag = False
        
for cat in range(len(cats)):
    print "Navigating to category " + cats[cat]+"\n"
    br.get(cats[cat])
    time.sleep(3)
    print "\nFlag value is currently " + str(flag) + "\n"
    time.sleep(1)
    # check if morecat visible
    tgl_c = [r.get_attribute("href") for r in br.find_elements_by_css_selector("#content > div > div.page_content > div > div.col-md-3.col-md-pull-9.col-sm-4.col-sm-pull-8 > div > div > ul.tgl_c li a")]
    if not tgl_c:
        print "\nGetting items directly.\n"
        list = br.find_elements_by_css_selector("#content > div > div > div.row > div > div > div.row.view-grid.animated.fadeInUp.animation-done > div > div > div.box_1 > form > div > a")
        for x in list:
            xt = x.get_attribute("href")
            print xt
            items.append(xt)
        while True:
            try:
                btn = br.find_element_by_link_text("Next")
                if btn.get_attribute("class") == "next disabled":
                    break
                    print "Pagination maxed out."
                time.sleep(1)
                btn.click()
                print "Page clicked."
                time.sleep(1)
                list = br.find_elements_by_css_selector("#content > div > div > div.row > div > div > div.row.view-grid.animated.fadeInUp.animation-done > div > div > div.box_1 > form > div > a")
                for x in list:
                    xt = x.get_attribute("href")
                    print xt
                    items.append(xt)
            except:
                print "\nPagination exhausted.\n"
                time.sleep(1)
                break
        print "\nSuccess getting items directly!\n"
        time.sleep(3)
    else:       
        morecat = [mc.get_attribute("href") for mc in br.find_elements_by_css_selector("#content > div > div.page_content > div > div.col-md-9.col-md-push-3.col-sm-8.col-sm-push-4 > div > div > table > tbody > tr > td > div > a")]
        print morecat
        print "\nMorecat found..\n"
        time.sleep(1)
        for ct in morecat:
            print "Morecat for loop executed..."
            time.sleep(1)
            print ct
            br.get(ct)
            time.sleep(1)
            list = br.find_elements_by_css_selector("#content > div > div > div.row > div > div > div.row.view-grid.animated.fadeInUp.animation-done > div > div > div.box_1 > form > div > a")
            for x in list:
                xt = x.get_attribute("href")
                print xt
                items.append(xt)
            while True:
                try:
                    btn = br.find_element_by_link_text("Next")
                    if btn.get_attribute("class") == "next disabled":
                        break
                        print "Pagination maxed out."
                    time.sleep(1)
                    btn.click()
                    print "Page clicked."
                    time.sleep(1)
                    list = br.find_elements_by_css_selector("#content > div > div > div.row > div > div > div.row.view-grid.animated.fadeInUp.animation-done > div > div > div.box_1 > form > div > a")
                    for x in list:
                        xt = x.get_attribute("href")
                        print xt
                        items.append(xt)
                except:
                    print "\nPagination exhausted.\n"
                    time.sleep(1)
                    break
                
            
            
            
            
            
for it in set(items):        
    print "Retrieving attributes from " + str(it)
    while True:
        try:
            br.get(it)
            time.sleep(1)
            get_info(br,table)
            break
        except:
            br.refresh()
            time.sleep(3)
            continue
    
        
outfile = open("./csv/outfile/images/olivias-heartland-wholesale_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)     
print "***Job Done!***"   