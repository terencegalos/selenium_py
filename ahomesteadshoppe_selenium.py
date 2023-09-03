from selenium import webdriver
import time
import urllib
import requests
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains


url = "http://www.ahomesteadshoppe.com/"
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
	name = driver.find_element_by_css_selector("#productName").text.encode("utf-8")
	sku = driver.find_element_by_css_selector("ul.floatingBox.back li").text.encode("utf-8")
	cat = driver.find_element_by_css_selector("#navBreadCrumb").text.encode("utf-8")
	try:
		dim = driver.find_element_by_css_selector("#productDetailsList li:nth-child(2)").text.encode("utf-8")
	except:
		dim = "No dim."
	min = driver.find_element_by_css_selector("#cartAdd > input[type=\"text\"]:nth-child(3)").get_attribute("value")
	price = driver.find_element_by_css_selector("#productPrices > span").text.encode("utf-8")
	try:
		image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#productMainImage a")))
		image = image.get_attribute("href")
	except:
		image = "none"
	ls = []
	ls.append(name)
	ls.append(sku.split("#")[1])
	ls.append("|".join([c.strip() for c in cat.split(">")]))
	ls.append(dim)
	ls.append(min)
	ls.append(price)
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

file = open("./csv/outfile/noimg/A_Homestead_Shoppe.csv","rb")

reader  = csv.reader(file)
for i in reader:
	try:
		time.sleep(1)
		br.find_element_by_name("keyword").clear()
		br.find_element_by_name("keyword").send_keys(i[1])
		br.find_element_by_name("keyword").send_keys(Keys.ENTER)
		time.sleep(1)
		itm = br.find_elements_by_css_selector("h3.itemTitle a")
		for x in itm:
			item = x.get_attribute("href")
			print item                
			items.append(item)
	except:
		print "No item found."
		
for i in set(items):
    print i
    get_info(br,i,table)
          
print "***Job Done***"
              
        
        
outfile = open("./csv/outfile/ahomesteadshoppe_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)