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



login = "http://desma-group.com/customer/account/login/"
url = "http://www.seventhmusewholesale.com/"
uname = "rick@waresitat.com"
passw = "seventhmuse"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
    
def init_login(driver,un,pw):
	print "Navigating to " + str(url) + " and logging in..."
	driver.get(url)
	print "Logging in."
	try:
		WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#enterPasswordDialoginputWithValidation1input"))).send_keys(pw)
		driver.find_element_by_css_selector("#enterPasswordDialogsubmitButton").click()
		time.sleep(5)
		print "Logged in."
	except:
		print "Success."
		driver.close()
        
        
def get_info(driver,sb,out):
	if sb == 0:
		item = [s.get_attribute("href") for s in driver.find_elements_by_css_selector("a.s38link")]
		descs = [s.text for s in driver.find_elements_by_css_selector("div.s5") if s != driver.find_elements_by_css_selector("div.s5")[0]]
		catdesc = driver.find_elements_by_css_selector("div.s5")[0]
		
		for it in range(len(item)):
			ls = []
			driver.get(item[it])
			time.sleep(1)
			
			ls.append(descs[it].split("\n"))
			ls.append(driver.find_element_by_css_selector("div.s82imageItemimage img").get_attribute("src"))
			out.append(ls)
			print ls
			ActionChains(driver).move_to_element(driver.find_element_by_css_selector("div.s82imageItemimage img")).perform()
			time.sleep(1)
			
	elif sb == 1 or sb == 2:
		print "Skipped sub 1 or 2"
	else:
		item = driver.find_elements_by_css_selector("div.vBOX.flex_display.flex_vbox")
		images = driver.find_elements_by_css_selector("div.vBOX.flex_display.flex_vbox img")
		description = []
		desc = driver.find_elements_by_css_selector("div.s5")
		for d in desc:
			description.append(d.text.encode("utf-8"))

		for itm in range(len(item)):
			ls = []
			txt = item[itm].text.encode("utf-8")
			ls.append(txt)
			ls.append(description)
			ls.append(images[itm].get_attribute("src"))
			print ls
			out.append(ls)
        
###################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
links = ["http://www.seventhmusewholesale.com/#!medallion-rings/cw6m","http://www.seventhmusewholesale.com/#!cameo-rings/c1stu","http://www.seventhmusewholesale.com/#!medallion-rings/cw6m","http://www.seventhmusewholesale.com/#!birthstone/c19bg","http://www.seventhmusewholesale.com/#!cameo-earrings/c1lep","http://www.seventhmusewholesale.com/#!tear-drop-earrings/c1ln8","http://www.seventhmusewholesale.com/#!card-necks/c46w","http://www.seventhmusewholesale.com/#!mala-necklaces/c1qb5","http://www.seventhmusewholesale.com/#!jewelry/cjg9","http://www.seventhmusewholesale.com/#!perfume-oils/cee5","http://www.seventhmusewholesale.com/#!mists/c1qs2"]
ln = "http://www.seventhmusewholesale.com/#!medallion-rings/cw6m"
s3link = "http://www.seventhmusewholesale.com/#!jewelry/cjg9"
cameo = "http://www.seventhmusewholesale.com/#!cameo-earrings/c1lep"

br = init_driver()
init_login(br,uname,passw)
time.sleep(1)
print "Navigating to jewelry/cjg9..."
br.get(s3link)
print "Success. Waiting for 6 secs..."
time.sleep(6)

items = []
table = []

images = []
names = []
prices = []
txtarr = []
cats = []

ActionChains(br).move_to_element(br.find_element_by_xpath("//*[@id=\"DrpDwnMn01\"]")).perform()
time.sleep(1)
submenu = br.find_elements_by_css_selector("div#DrpDwnMn0moreContainer a")

for sub in range(len(submenu)):
	ActionChains(br).move_to_element(br.find_element_by_xpath("//*[@id=\"DrpDwnMn01\"]")).perform()
	ActionChains(br).move_to_element(br.find_elements_by_css_selector("div#DrpDwnMn0moreContainer a")[sub]).perform()
	br.find_elements_by_css_selector("div#DrpDwnMn0moreContainer a")[sub].click()
	time.sleep(5)
	
	get_info(br,sub,items)
	br.get(s3link)
	time.sleep(1)
	
outfile = open("./csv/outfile/seventhmuse_results_2.csv","wb")
writer = csv.writer(outfile)
writer.writerows(items)

print "***Job Done***"
br.close()