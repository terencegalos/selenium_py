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

url = "https://www.goldenhillstudio.com/"
uname = "rick@waresitat.com"
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    br.get("https://www.ahomesteadshoppe.com/index.php?main_page=login")
    time.sleep(1)
    print "Logging in."
    
    driver.find_element_by_name("email_address").send_keys(un)
    driver.find_element_by_name("password").send_keys(pw)
    driver.find_element_by_css_selector("#loginForm div.buttonRow.forward input[type=\"image\"]").click()
    time.sleep(5)
    print "Logged in."

def get_info(key,driver,link,out):
    print "Navigating to: \n" + str(link)
    driver.get(link)
    time.sleep(1)  
    
    try:
        sku = driver.find_element_by_css_selector("#ProductItemCode").text.encode("utf-8")
    except:
        sku = "None"

    try:
        cat = driver.find_element_by_css_selector("#commerce div div.BackToCategory a").text.encode("utf-8")    
    except:
        cat = "None"
        
    dim = br.find_element_by_css_selector("#commerce div table tbody tr td:nth-child(2) table:nth-child(1) tbody tr:nth-child(2) td table tbody tr:nth-child(1) td:nth-child(2)").text.encode("utf-8")

    try:
        image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#COMProdImage")))
        image = image.get_attribute("src")
    except:
        image = "none"
        

    ls = []
    
    ls.append(key)

    ls.append(sku)
    
    ls.append(cat)
    
    ls.append(dim)

    ls.append(image)
    
    print ls
    
    out.append(ls)


    
    
####################################################################################################################################################################################################################################
    
                
br = init_driver()
time.sleep(1)

br.get(url)
print "Waiting for homepage to load..."
time.sleep(3)


items = []
table = []
cats = []

with open("./csv/infile/goldenhill.csv","rb") as infile:
	for i in infile:
		try:
			time.sleep(1)
			br.find_element_by_name("q").clear()
			br.find_element_by_name("q").send_keys(i)
			time.sleep(1)
			x = br.find_element_by_css_selector("body > div.container.content.container-header > div:nth-child(2) > div > div.one-third.column.alpha.thumbnail.even > a").get_attribute("href")
			time.sleep(1)
			print x
			br.get(x)
			time.sleep(1)
			ls = []
			ls.append(i.strip())
			ls.append(br.find_element_by_css_selector("img.cloudzoom.featured_image").get_attribute("src"))
			print ls
			table.append(ls)
		except:
			print "No item found."

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
              
        
        
outfile = open("./csv/outfile/goldenhillstudio.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)