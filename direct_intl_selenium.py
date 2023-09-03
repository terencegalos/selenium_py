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



login = "http://www.americaretold.com/index.php/retailer-access.html"
url = "http://directinternationalinc.com/"
uname = "7261"
passw = "N0G1A0"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser
    
    
def init_login(driver,un,pw):
	driver.find_element_by_link_text("Log In").click()
	time.sleep(1)
	print "Logging in."
	try:
		WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME,"u"))).send_keys(un)
		WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME,"p"))).send_keys(pw)
		WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME,"btnLogin"))).click()
		time.sleep(1)
		print "Sucess."
	except:
		print "Failed."
		driver.close()
        
        
def get_items(driver,out):
	#get items the first time
	it = [i.get_attribute("href") for i in driver.find_elements_by_css_selector("#frmCompare ul li div.ProductDetails strong a")]
	for i in list(set(it)):
		out.append(i)
		print i
	#click next page until exhausted
	while True:
		try:
			driver.find_element_by_css_selector("#CategoryPagingBottom div div.FloatRight a").click()
			time.sleep(1)
			print "Next page clicked.."
			it = [i.get_attribute("href") for i in driver.find_elements_by_css_selector("#frmCompare ul li div.ProductDetails strong a")]
			for i in list(set(it)):
				out.append(i)
				print i
		except:
			print "Next page exhausted."
			time.sleep(1)
			break

def get_info(driver,num,out):
	ls = []
	link = driver.find_elements_by_css_selector("div.CONTENT div.bi.clearfix div.b div.bi.clearfix")[num]
	try:
		name = link.find_element_by_css_selector("div.bt h2").text.encode("utf-8")
		sku = link.find_element_by_css_selector("tr.sku td:nth-child(2)").text.encode("utf-8")
		status = link.find_element_by_css_selector("tr.status td:nth-child(2)").text.encode("utf-8")
		try:
			inner = link.find_element_by_css_selector("tr.inner td:nth-child(2)").text.encode("utf-8")
		except:
			inner = "No inner."
		price = link.find_element_by_css_selector("tr.price td:nth-child(2)").text.encode("utf-8")
		try:
			case = link.find_element_by_css_selector("tr.outter td:nth-child(2)").text.encode("utf-8")
		except:
			case = "No case."
		image = link.find_element_by_css_selector("img").get_attribute("src").replace("thumb","full")

		ls.append(name)
		ls.append(sku)
		ls.append(driver.find_element_by_xpath("//*[@id=\"body\"]/div[2]/div/div/div/div[4]/div/div[2]/div/div[1]/div/h1").text.encode("utf-8"))
		ls.append(status)
		ls.append(price)
		ls.append(inner)
		ls.append(case)
		ls.append(image.replace("images/","common/zoom.html?image=%2Fimages%2F"))
		print ls
		out.append(ls)
	except:
		print "Error getting item info. Displaying content...."
		time.sleep(1)
		print link.get_attribute("innerHTML")
		time.sleep(3)
		
        
###################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

br = init_driver()
br.get(url)
time.sleep(1)
init_login(br,uname,passw)
time.sleep(4)

table = []
items = []
section = [i.get_attribute("href") for i in br.find_elements_by_css_selector("#body div div div div div.b.bc8.MAIN.BOF.biil10 div div.b.bc8.bid29.CONTENT.BOF.biil10.bw80 div div div div a")]
for sect in section:
	print "Navigating to " + sect
	br.get(sect)
	time.sleep(1)
	#get info once
	item = br.find_elements_by_css_selector("div.CONTENT div.bi.clearfix div.b div.bi.clearfix")
	for i in range(len(item)):
		get_info(br,i,table)
	#get all pages
	page = [p.get_attribute("href") for p in br.find_elements_by_css_selector("div.b.bc800.biil10 div.bi.clearfix ul li a")]
	for x in range(len(page)):
		try:
			print x
			time.sleep(3)
			#click next page and get all info
			# page = len(br.find_elements_by_css_selector("div.bi.clearfix ul li a"))
			# br.find_elements_by_css_selector("div.bi.clearfix ul li a")[page-1].click()
			br.get(page[x])
			time.sleep(5)
			item = br.find_elements_by_css_selector("div.CONTENT div.bi.clearfix div.b div.bi.clearfix")
			for i in range(len(item)):
				get_info(br,i,table)
		except:
			print "Page exhausted."
			time.sleep(3)
				
outfile = open("./csv/outfile/directinternationalinc.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"
br.close()