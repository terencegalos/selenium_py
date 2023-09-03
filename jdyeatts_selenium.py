import webdriver_config
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

url = "https://www.jdyeatts.com/"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    driver.get(url)
    print "Logging in."
    while True:
        try:
            driver.find_element_by_name("LOG_ID").clear()
            driver.find_element_by_name("PASSWORD").clear()
            
            ActionChains(driver).move_to_element(driver.find_element_by_name("LOG_ID")).perform()
            driver.find_element_by_name("LOG_ID").send_keys(un)
            time.sleep(5)
            # ActionChains(driver).move_to_element(driver.find_element_by_name("PASSWORD")).perform()
            # driver.find_element_by_name("PASSWORD").send_keys("wolfville")
            time.sleep(1)
            break
        except Exception as e:
            br.refresh()
            print e
            time.sleep(1)
            continue
    time.sleep(3)
    print "Success."
    
def get_info(driver,out):
    ls = []
    # driver.get(i)
    # print "Navigating to:\n" + str(i)
    
    # time.sleep(1)
    # title = driver.find_element_by_css_selector("h2.title").text.encode("utf-8")
    sku = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div > div.product-info > table > tbody > tr:nth-child(1) > td:nth-child(3)"))).text.encode("utf-8")
    # desc = driver.find_element_by_css_selector("#ProductDescription div").text.encode("utf-8")
    # price = driver.find_element_by_css_selector("#ProductDetails div div.ProductMain div.ProductDetailsGrid div.p-price div.DetailRow.PriceRow div em.ProductPrice.VariationProductPrice").text.encode("utf-8")
    
    # ActionChains(driver).move_to_element(driver.find_element_by_css_selector("#TinyImage_0")).perform()
    # time.sleep(1)
    
    image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,"large_picture"))).get_attribute("src")

    # ls.append(title)
    ls.append(sku.split("\n")[0])
    # ls.append(desc)
    # ls.append(price)
    ls.append(image)
    out.append(ls)
    print ls
    # try:
        # option = [btn.text.encode("utf-8") for btn in driver.find_elements_by_css_selector("div.productAttributeValue > div > ul > li > label > span.name")]
        # print option
        # print "Status: More options detected."
        # time.sleep(1)
        # for x in range(len(option)):
            # print x
            # ls = []
            # driver.find_elements_by_css_selector("div.productAttributeValue > div > ul > li")[x].click()
            # time.sleep(2)
            
            # sku = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#productDetailsAddToCartForm div div.DetailRow.ProductSKU div.Value span"))).text.encode("utf-8")
            # price = driver.find_element_by_css_selector("#ProductDetails div div.ProductMain div.ProductDetailsGrid div.p-price div.DetailRow.PriceRow div em.ProductPrice.VariationProductPrice").text.encode("utf-8")
            
            # ls.append(title)
            # ls.append(sku)
            # ls.append(desc)
            # ls.append(price)
            # ls.append(image)
            # out.append(ls)
            # print ls
    # except Exception as e:
        # print e
        # time.sleep(1)
         

br = webdriver_config.init_driver()
br.get(url)
time.sleep(2)
init_login(br,uname,passw)

table = []

with open("./csv/infile/jdy.csv","rb") as infile:
    for i in infile:
        print "\nSearching for product: " + i + "\n"
        br.find_element_by_name("I_PROD_DESC").send_keys(i.split(",")[1])
        time.sleep(1)
        br.find_element_by_css_selector("body > div.category-results > center > form > table > tbody > tr > td > div > div.p-name > a").click()
        time.sleep(1)
        get_info(br,out)



print "***Job Done***"        
        
outfile = open("./csv/outfile/images/jdy_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()