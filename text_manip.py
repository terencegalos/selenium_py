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

items = {}
table = []
cats = []
with open("./csv/infile/thompsons2.csv","rb") as scents:
	for scent in scents:
		sc = scent.split(",")
		with open("./csv/infile/thompsons1.csv","rb") as items:
			for item in items:
				it = item.split(",")
				ls = []
				ls.append(sc[1].strip() + " " + it[1])
				ls.append(sc[0]+it[0])
				ls.append(sc[2].strip())
				ls.append(it[2].strip())
				print ls
				table.append(ls)
        
        
outfile = open("./csv/outfile/text_manip_result.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)