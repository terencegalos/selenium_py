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



url = "https://www.barncandles.com/"
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


        
br = init_driver()
init_login(br,uname,passw)
br.get(url)
time.sleep(3)
# btn = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ctl37_rpLinkList_ctl00_dvHorizontalNavItem a")))
# btn.click()
# time.sleep(2)



items = []
table = []
# links = ["https://www.barncandles.com/store/c/66-Barn-Candles.aspx","https://www.barncandles.com/store/c/31-Barn-Bricks.aspx","https://www.barncandles.com/store/c/32-Barn-Diffusers.aspx","https://www.barncandles.com/store/c/33-Barn-Room-Spray.aspx","https://www.barncandles.com/store/c/28-Accessories.aspx","https://www.barncandles.com/store/c/43-Kitchen-Pantry.aspx","https://www.barncandles.com/store/c/36-Reflective-Light-Inspirations.aspx","https://www.barncandles.com/store/c/41-Reflective-Light-Inspirations-Diffuser.aspx","https://www.barncandles.com/store/c/37-Reflective-Light-Inspirations-Room-Spray.aspx","https://www.barncandles.com/store/c/38-Reflective-Light-Scentiments.aspx","https://www.barncandles.com/store/c/40-Reflective-Light-Scentiments-Room-Spray.aspx",]



# for i in links:
    # br.get(i)
    # time.sleep(1)
    # view100 = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ddShowByPageSize option:nth-child(5)")))
    # view100.click()
    # WebDriverWait(br,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#dlCategory tbody tr:nth-child(1) td:nth-child(1) div div.CategoryProductNameLink a")))
    # item = br.find_elements_by_css_selector("div.CategoryProductNameLink a")
    # for i in item:
        # items.append(i.get_attribute("href"))
        # print i.get_attribute("href")

    


with open("./csv/infile/barncandlesku.csv","rb") as infile:
    for i in infile:
        ls = []
        br.find_element_by_id("txtRedirectSearchBox").clear()
        br.find_element_by_id("txtRedirectSearchBox").send_keys(i)
        print "Searching for " + str(i)
        time.sleep(1)
        
        try:
            input = i
            name = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#MainForm div.Layout section section div.LayoutContentInner h1")))
            sku = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#lblItemNr")))
            cat = br.find_element_by_css_selector("#lblCategoryTrail")
            desc = br.find_element_by_css_selector("#tabs-1")
            try:
                say = br.find_element_by_css_selector("#lblBullets em")
            except:
                say = "None"
            vary = br.find_elements_by_css_selector("select.variantDropDown_30 option")
            variation = []
            try:
                for i in vary:
                    variation.append(i.text.encode("utf-8"))
            except:
                variation.append("None")
            min = br.find_element_by_css_selector("#txtQuantity")
            price = br.find_element_by_css_selector("#lblPrice")
            image = WebDriverWait(br,2).until(EC.visibility_of_elemfent_located((By.CSS_SELECTOR,"#PhotoThumbnails_lnkProductPhotoZoom")))

            ls.append(input)
            ls.append(name.text.encode("utf-8"))
            ls.append(sku.text.encode("utf-8"))
            ls.append(cat.text.encode("utf-8"))
            ls.append(desc.text.encode("utf-8"))
            try:
                ls.append(say.text.encode("utf-8"))
            except:
                ls.append(say)
            ls.append(variation)
            ls.append(min.get_attribute("value"))
            ls.append(price.text.encode("utf-8"))
            ls.append(image.get_attribute("href"))
            table.append(ls)
            print ls
            
        except:
            try:
                br.find_element_by_css_selector("div.CategoryProductNameLink a").click()
            except:
                continue
            time.sleep(1)
            
            input = i
            name = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#MainForm div.Layout section section div.LayoutContentInner h1")))
            sku = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#lblItemNr")))
            cat = br.find_element_by_css_selector("#lblCategoryTrail")
            desc = br.find_element_by_css_selector("#tabs-1")
            try:
                say = br.find_element_by_css_selector("#lblBullets em")
                #lblBullets > p > em
            except:
                say = "None"
            vary = br.find_elements_by_css_selector("select.variantDropDown_30 option")
            variation = []
            try:
                for i in vary:
                    variation.append(i.text.encode("utf-8"))
            except:
                variation.append("None")
            min = br.find_element_by_css_selector("#txtQuantity")
            price = br.find_element_by_css_selector("#lblPrice")
            image = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#PhotoThumbnails_lnkProductPhotoZoom")))

            ls.append(input)
            ls.append(name.text.encode("utf-8"))
            ls.append(sku.text.encode("utf-8"))
            ls.append(cat.text.encode("utf-8"))
            ls.append(desc.text.encode("utf-8"))
            try:
                ls.append(say.text.encode("utf-8"))
            except:
                ls.append(say)
            ls.append(variation)
            ls.append(min.get_attribute("value"))
            ls.append(price.text.encode("utf-8"))
            ls.append(image.get_attribute("href"))
            table.append(ls)
            print ls



print "***Job Done***"        
        
outfile = open("./csv/outfile/barncandles2.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)