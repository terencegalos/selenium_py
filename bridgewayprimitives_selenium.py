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


url = "http://www.bridgewayprimitiveswholesale.com/store/"
login = "http://bridgewayprimitiveswholesale.com/store/index.php?route=account/login"
uname = "tamara.salvetti@yahoo.com"
passw = "teacherk1"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    br.get(login)
    time.sleep(1)
    print "Logging in."
    
    driver.find_element_by_name("email").send_keys(un)
    driver.find_element_by_name("password").send_keys(pw)
    driver.find_element_by_css_selector("#content div.login-content div.right form div input.button").click()
    time.sleep(5)
    print "Logged in."

def get_info(driver,link,out):    
    print "Navigating to: \n" + str(link)
    driver.get(link)
    time.sleep(1)
    
    name = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#content > h1")))
    
    try:
        sku = driver.find_element_by_xpath("//*[@id=\"content\"]/div[2]/div[2]/div[1]/text()[1]")
    except:
        sku = "None"

    cat = driver.find_element_by_css_selector("div.breadcrumb").text.encode("utf-8")
    
    try:
        desc = driver.find_element_by_css_selector("div.description").text.encode("utf-8")
    except:
        desc = "None"    
    # try:
        # set = driver.find_element_by_xpath("//*[@id=\"MainForm\"]/div[2]/section/section/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div/text()").text.encode("utf-8")
    # except:
        # set = "None."
  
    try:
        qty = driver.find_element_by_name("quantity").get_attribute("value")
    except:
        qty = "None"     
    
    try:
        price = driver.find_element_by_css_selector("div.price").text.encode("utf-8")
    except:
        price = "None."

    try:
        image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.image a")))
        image = image.get_attribute("href")
    except:
        image = "none"
        

    ls = []
    
    ls.append(name.text.encode("utf-8"))

    ls.append(sku)
    
    ls.append(cat)

    ls.append(desc)
    
    ls.append(set)
    
    ls.append(qty)

    ls.append(price)

    ls.append(image)
    
    varies = []
    
    try:
    
        var = driver.find_elements_by_css_selector("div.options div.option select")
        for i in var:
            lis = []
            vary = i.text.splitlines()
            for i in vary:
                lis.append(i.strip())
            varies.append(lis)
        varlen = len(var)
        print "Options found. Total number of option/s: " + str(varlen)
        
        # for x in range(1,varlen):
            # print "X is: " + str(x)
            # lis = []
            
            # if varlen == 1:
                # vary = driver.find_elements_by_css_selector("div.options div.option select option")
            # else:
                # vary = driver.find_elements_by_css_selector("div.options div.option:nth-child("+str(x)+") select option")
            
            # for i in vary:
                # print i.text
            
            # for i in vary:
                # opt = i.text.encode("utf-8")
                # lis.append(opt)
                # print lis
            # varies.append(lis)
        
        #appending all options
        for i in varies:
            ls.append(i)

        
    except:
        print "No options found."
    
    
    
    print ls
    
    out.append(ls)


    
    
####################################################################################################################################################################################################################################
    
                
br = init_driver()
init_login(br,uname,passw)
br.get("http://www.bridgewayprimitiveswholesale.com/store/")
print "Waiting for homepage to load..."
time.sleep(3)


items = []
table = []
cats = []
    
# rawitems = br.find_elements_by_css_selector("div.box-category ul li a")
# for i in rawitems:
    # itm = i.get_attribute("href")
    # print itm
    # if itm == "http://bridgewayprimitiveswholesale.com/store/fragrance-descriptions-":
        # continue
        # print "Skipping..."
    # else:
        # cats.append(itm)
    
# print "Categories has been saved. Scraping each for items..."
# with open("./csv/infile/bridgewayprimitiveswholesale_items.csv","rb") as cats:
    # for i in cats:
        # print "Navigating to: " + str(i)
        # br.get(i)
        # time.sleep(1)
        # try:
            # print "Looking for more items..."
            # br.find_element_by_css_selector("#content div.product-filter div.limit select option:nth-child(5)").click()
        # except:
            # print "Nothing more found. Getting all items in this page..."
        # time.sleep(1)
        # item = br.find_elements_by_css_selector("div.image a")
        # for i in item:
            # itm = i.get_attribute("href")
            # items.append(itm)
            # print itm
        # print "All items in this category has been scraped. Going to the next category..."

# print "**All items from this website has been saved.**"    

# items = list(set(items))

# outfile1 = open("./csv/outfile/bridgewayprimitiveswholesale_items.csv","wb")
# writer1 = csv.writer(outfile1)
# writer1.writerow(items)

with open("./csv/infile/bridgewayprimitiveswholesale_items.csv","rb") as cats:
    for i in cats:
        while True:
            try:
                get_info(br,i,table)
            except:
                br.refresh()
                time.sleep(1)
                continue
            else:
                break

# except:
    # list = []   
    # br.find_element_by_css_selector("#ddShowByPageSize option:nth-child(5)").click()
    # time.sleep(1)
    # item = br.find_elements_by_css_selector("div.no-m-b a")
    # print "More items found.."
    # for i in item:
        # itm = i.get_attribute("href")
        # list.append(itm)
        # print itm   
    # for i in list:
        # try:
            # get_info(br,i,table)
        # except:
            # continue

            
print "***Job Done***"
              
        
        
outfile = open("./csv/outfile/bridgewayprimitiveswholesale2.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)