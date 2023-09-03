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


url = "http://www.simplycountrydesignswholesale.com/"
login = "http://www.simplycountrydesignswholesale.com/"
uname = "rick@waresitat.com"
passw = "wolfville4"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    driver.get(url)
    time.sleep(1)
    print "Logging in."
    driver.find_element_by_css_selector("#home div.page div.header div div.TopMenu div ul li:nth-child(5) div a:nth-child(1)").click()
    time.sleep(2)
    
    driver.find_element_by_id("login_email").send_keys(un)
    driver.find_element_by_name("login_pass").send_keys(pw)
    driver.find_element_by_id("LoginButton").click()
    time.sleep(5)
    print "Logged in."

def get_info(driver,link,out):    
    print "Navigating to: \n" + str(link)
    driver.get(link)
    time.sleep(1)
    
    name = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ProductDetails div div.ProductMain div.ProductDetailsGrid div.DetailRow.product-heading h1"))).text.encode("utf-8")
    
    try:
        sku = driver.find_element_by_css_selector("#productDetailsAddToCartForm div div.DetailRow.ProductSKU div.Value span").text.encode("utf-8")
    except:
        sku = "No SKU."

    cat = driver.find_element_by_css_selector("#ProductBreadcrumb").text.encode("utf-8")
    
    try:
        desc = driver.find_element_by_css_selector("#ProductDescription div").text.encode("utf-8")
    except:
        desc = "No Description."    
  
    try:
        qty = driver.find_element_by_css_selector("#qty_ option").text.encode("utf-8")
    except:
        qty = "No minimum."     
    
    try:
        price = driver.find_element_by_css_selector("#ProductDetails div div.ProductMain div.ProductDetailsGrid div.DetailRow.PriceRow.p-price div span.ProductPrice.VariationProductPrice").text.encode("utf-8")
    except:
        price = "No Price."

    try:
        image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ProductDetails div div.left-content div div.ProductThumbImage a img"))).get_attribute("src")
    except:
        image = "No Image."
        
    try:
        options = []
        option = br.find_elements_by_css_selector("div.productAttributeValue div ul li label span.textureContainer.showPreview")
        for opt in option:
            op = opt.get_attribute("title")
            print op
            options.append(op)
    except:
        print "No option available for this item."
        

    ls = []
    
    ls.append(name)

    ls.append(sku)
    
    ls.append(cat)

    ls.append(desc)
    
    ls.append(qty)

    ls.append(price)

    ls.append(image)
    
    ls.append(options)    
    
    print ls
    
    out.append(ls)


    
    
####################################################################################################################################################################################################################################

br = init_driver()
init_login(br,uname,passw)

cats = []
items = []
table = []

skupair = []

catseek = []

with open("./csv/infile/scp_infile.csv","rb") as infile:
    for i in infile:
        ls = []
        print i
        br.get(i)
        time.sleep(1)
        try:
            sk = br.find_element_by_css_selector("#productDetailsAddToCartForm div div.DetailRow.ProductSKU div.Value span").text.encode("utf-8")
        except:
            sk = "No sku"
        ls.append(i)
        ls.append(sk)
        skupair.append(ls)
        print ls
      

outfile = open("./csv/outfile/simplycountrydesignswholesale_sku_cat_pair.csv","wb")
writer = csv.writer(outfile)
writer.writerows(skupair)

            
print "***Job Done***"
              
      
