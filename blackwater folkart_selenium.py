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


login = "http://www.blackwaterfolkart.com/index.php?route=account/login"
url = "http://www.blackwaterfolkart.com/index.php?route=information/information&information_id=10"
uname = "rick@waresitat.com"
passw = "wolfville"




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

def get_info(key,driver,link,out):
    print "Navigating to: \n" + str(link)
    driver.get(link)
    time.sleep(1)  
    
    try:
        desc = driver.find_element_by_css_selector("#content div.product-info div.right div.description").text.encode("utf-8")
    except:
        desc = "None"

    try:
        cat = driver.find_element_by_css_selector("div.breadcrumb").text.encode("utf-8")    
    except:
        cat = "None"
        
    # dim = br.find_element_by_css_selector("#commerce div table tbody tr td:nth-child(2) table:nth-child(1) tbody tr:nth-child(2) td table tbody tr:nth-child(1) td:nth-child(2)").text.encode("utf-8")

    try:
        image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#content div.product-info div.left div a")))
        image = image.get_attribute("href")
    except:
        image = "none"
        

    ls = []
    
    ls.append(key)

    ls.append(desc)
    
    ls.append(cat)
    
    # ls.append(dim)

    ls.append(image)
    
    print ls
    
    out.append(ls)


    
    
####################################################################################################################################################################################################################################
    
                
br = init_driver()
init_login(br,uname,passw)
time.sleep(1)

br.get(url)
print "Waiting for homepage to load..."
time.sleep(3)


items = []
table = []
cats = []

with open("./csv/infile/blackwater.csv","rb") as infile:
    for i in infile:
		time.sleep(1)
		br.find_element_by_name("search").clear()
		br.find_element_by_name("search").send_keys(i)
		time.sleep(1)
		item = [i.get_attribute("href") for i in br.find_elements_by_css_selector("div.name a")]
		print item
		items.extend(item)
			
			
for i in set(items):
	while True:
		try:
			get_info(i,br,item,table)
			break
		except:
			br.refresh()
			time.sleep(1)
			continue


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
              
        
        
outfile = open("./csv/outfile/blackwater_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)