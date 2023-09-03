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


url = "http://www.desperate.com/shophome.cfm"
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

def get_info(driver,link,out):
    print "Navigating to: \n" + str(link)
    driver.get(link)
    time.sleep(1)  
    
    try:
        sku = driver.find_element_by_xpath("/html/body/table[3]/tbody/tr[1]/td[2]/div/center/table/tbody/tr/td[2]/form[1]/font/text()[3]")
    except:
        sku = "None"

    try:
        cats = []
        cat = driver.find_elements_by_css_selector("body table:nth-child(4) tbody tr:nth-child(1) td:nth-child(1) b")   
        for i in cat:
            cats.append(i.text.encode("utf-8"))
    except:
        cats = "None"
        
    dim = br.find_element_by_css_selector("div#productDetailsList").text.encode("utf-8")

    try:
        image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#productMainImage a")))
        image = image.get_attribute("href")
    except:
        image = "none"
        

    ls = []
    

    ls.append(sku)
    
    ls.append(cats)
    
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
catstring = []

with open("./csv/infile/desperate.csv","rb") as infile:
	for i in infile:
		print "Notice: Searching for item " + str(i)
		while True:
			try:
				br.find_element_by_name("searchcriteria").clear()
				br.find_element_by_name("searchcriteria").send_keys(i)
				time.sleep(2)
				break
			except:
				br.refresh()
				time.sleep(1)
				continue
		try:
			ls = []
			br.find_element_by_css_selector("body > table:nth-child(4) > tbody > tr:nth-child(1) > td:nth-child(2) > div > center > table > tbody > tr > td > div > center > table:nth-child(3) > tbody > tr > td > a").click()
			time.sleep(1)
			item = br.find_element_by_css_selector("body > table:nth-child(4) > tbody > tr:nth-child(1) > td:nth-child(2) > div > center > table > tbody > tr > td:nth-child(2) > form:nth-child(1) > font").text.encode("utf-8")
			sku = item.splitlines()[-1:]
			image = br.find_element_by_css_selector("body > table:nth-child(4) > tbody > tr:nth-child(1) > td:nth-child(2) > div > center > table > tbody > tr > td:nth-child(2) > form:nth-child(1) > a:nth-child(2) > img").get_attribute("src")
			ls.append(sku[0].split()[-1:])
			ls.append(image)
			print ls
			table.append(ls)
		except:
			print "Status: Item not found."

print "***Job Done***"
              
        
        
outfile = open("./csv/outfile/desperate_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)