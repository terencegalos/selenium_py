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


url = "http://www.packagingsource.com/"
uname = "rick@waresitat.com"
passw = "wolfville"


def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    br.get("http://barncandles.americommerce.com/")
    time.sleep(1)
    btn = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#utilnav ul li:nth-child(2) font b a")))
    btn.click()
    time.sleep(1)
    print "Logging in."
    
    driver.find_element_by_name("txtEmailAddress").send_keys(un)
    driver.find_element_by_name("txtPassword").send_keys(pw)
    driver.find_element_by_name("btnSignIn").click()
    time.sleep(5)
    print "Logged in."

def get_info(driver,link,out):    
    print "Navigating to: " + str(link)
    driver.get(link)
    time.sleep(1)
    name = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h1.ProductDetailsProductName.no-m-t")))
    
    sku = driver.find_element_by_id("lblItemNr").text.encode("utf-8")

    cat = driver.find_element_by_css_selector("div.breadcrumb").text.encode("utf-8")

    
    try:
        desc = driver.find_element_by_id("desc1").text.encode("utf-8")
    except:
        desc = "None"    
    try:
        set = driver.find_element_by_xpath("//*[@id=\"MainForm\"]/div[2]/section/section/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div/text()").text.encode("utf-8")
    except:
        set = "None."
  
    try:
        var = driver.find_elements_by_tag_name("option")
        vary = []
        for i in var:
            vary.append(i.text.encode("utf-8"))
        print vary[0]
    except:
        vary = "none"    

    try:
        qty = driver.find_element_by_name("txtQuantity").get_attribute("value")
    except:
        qty = "None"     

    price = driver.find_element_by_id("lblPrice").text.encode("utf-8")    

    try:
        image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a.main-product-photo.block.zoom.rel")))
        image = image.get_attribute("href")
    except:
        image = "none"
        
    try:
        if vary[0] == "Please Select Size":
            for i in vary:
                ls = []
                ls.append(name.text.encode("utf-8"))

                ls.append(i)

                ls.append(sku)

                ls.append(cat)

                ls.append(desc)
                
                ls.append(set)

                ls.append(qty)

                ls.append(price)

                ls.append(image)

                print ls
                out.append(ls)
        else:
            ls = []
            ls.append(name.text.encode("utf-8"))

            ls.append(vary)

            ls.append(sku)

            ls.append(cat)

            ls.append(desc)
            
            ls.append(set)

            ls.append(qty)

            ls.append(price)

            ls.append(image)

            print ls
            out.append(ls)
    except:
        ls = []
        ls.append(name.text.encode("utf-8"))
        ls.append(vary)
        ls.append(sku)
        ls.append(cat)
        ls.append(desc)
        ls.append(set)
        ls.append(qty)
        ls.append(price)
        ls.append(image)
        print ls
        out.append(ls) 
       
        
                
br = init_driver()
br.get(url)
time.sleep(3)
print "Waiting for homepage to load..."


items = []
table = []
    

with open("./csv/infile/thepackagingsource_items.csv","rb") as infile:
    for i in infile:
        try:
            get_info(br,i,table)
        except:
            try:
                list = []
                br.find_element_by_css_selector("#ddShowByPageSize option:nth-child(5)").click()
                time.sleep(1)
                item = br.find_elements_by_css_selector("div.no-m-b a")
                print "More items found.."
                for i in item:
                    itm = i.get_attribute("href")
                    list.append(itm)
                    print itm
                for i in list:
                    try:
                        get_info(br,i,table)
                    except:
                        continue
            except:
                continue

                
print "***Job Done***"
        
               
        
        
        
outfile = open("./csv/outfile/thepackagingsource_items_att4.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)