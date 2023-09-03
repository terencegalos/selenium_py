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



login = "http://www.sweetshoppecandles.com/#!password-protected/mjlxw"
url = "http://www.sweetshoppecandles.com/#!wholesale/j5nyx"
uname = "rick@waresitat.com"
passw = "sweetshoppe12"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
    
def init_login(driver,pw):
	print "Logging in..."
	driver.get(url)
	time.sleep(2)
	ActionChains(driver).move_to_element(driver.find_element_by_css_selector("#DrpDwnMn02label")).perform()
	driver.find_element_by_css_selector("#DrpDwnMn02_0label").click()
	time.sleep(3)
	WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#enterPasswordDialoginputWithValidation1input"))).send_keys(pw)
	driver.find_element_by_css_selector("#enterPasswordDialogsubmitButton").click()
	time.sleep(1)
	print "Success."
	
        
def get_items(driver,out):
	#get items the first time
	it = [i.get_attribute("href") for i in driver.find_elements_by_css_selector("#content table tbody tr td:nth-child(2) table tbody tr:nth-child(2) td table tbody tr:nth-child(7) td table tbody tr:nth-child(1) td table tbody tr td table tbody tr td.product-grid-text a")]
	for i in list(set(it)):
		out.append(i)
		print i

def get_info(driver,link,out):
	driver.get(link)
	time.sleep(1)
	driver.switch_to_frame(driver.find_elements_by_css_selector("div#SITE_PAGES iframe")[8])
	time.sleep(1)
	name = driver.find_element_by_css_selector("h1.product-name").text.encode("utf-8")
	desc = driver.find_element_by_css_selector("div.content-wrapper").text.encode("utf-8")
	min = driver.find_element_by_css_selector("body div section header div section product-options div form div div a span:nth-child(2) span").text.encode("utf-8")
	price = driver.find_element_by_css_selector("body div section header div section product-price div span").text.encode("utf-8")
	image = driver.find_element_by_css_selector("#magic-zoom-0 img").get_attribute("src")
    
	ls = []
	ls.append(name)
	ls.append(desc)
	ls.append(min)
	ls.append(price)
	ls.append(image)
	out.append(ls)
	print "\n"
	print [s for s in ls]
	print "\n"
        
###################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

br = init_driver()
time.sleep(1)
init_login(br,passw)
time.sleep(10)
table = []
items = []

frames = br.find_elements_by_css_selector("div#SITE_PAGES iframe")

for frame in frames:
	br.switch_to_frame(frame)
	time.sleep(1)
	item = [prod.get_attribute("href") for prod in br.find_elements_by_css_selector("div.product-media a") if prod.get_attribute("href") is not "None"]
	for it in item:
		try:
			items.append(it)
			print it
			time.sleep(0.5)
		except Exception as e:
			print e
			time.sleep(1)
	br.switch_to_default_content()

for itm in items:
	print "Getting info for:"
	print itm
	try:
		get_info(br,itm,table)
	except:
		print "Skipped."


outfile = open("./csv/outfile/sweetshoppe_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)		
	
print "***Job Done***"