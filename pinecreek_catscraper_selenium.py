from selenium import webdriver
import time
import urllib2
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from urllib import urlopen
import urllib
import csv

login = "https://adamsandco.net/home.php"
url = "http://www.shoppinecreek.com/"
uname = "rick@waresitat.com"
passw = "wolfville"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):
    time.sleep(3)
    print "Logging in..."
    time.sleep(1)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.NAME,"Customer_Login"))).send_keys(un)
    driver.find_element_by_name('Customer_Password').send_keys(pw)
    driver.find_element_by_css_selector("#logn div div div.sign-in-buttons input").click()
    print "Login Success."
    time.sleep(3)
    # except:
        # print "Login failed."
def get_info(driver,out):
	ls = []
	name = driver.find_element_by_css_selector("#product-header h1").text.encode("utf-8")
	sku = driver.find_element_by_css_selector("#main-content div.product-code span").text.encode("utf-8")
	try:
		cat = driver.find_element_by_css_selector("#main-content div:nth-child(5)").text.encode("utf-8")
	except:
		return
	try:
		minqty = driver.find_element_by_css_selector("#main-content > div.product-details-2 > form > div.purchase-buttons > select > option:nth-child(1)").get_attribute("value")
	except:
		minqty = "No minqty."
	try:
		price = driver.find_element_by_css_selector("#price-value").text.encode("utf-8")
	except:
		price = "No price."
	try:
		image = driver.find_element_by_id("main_image").get_attribute("src")
		print image
	except:
		image = "No image."
	
	ls.append(name)
	ls.append(sku)
	ls.append(cat)
	ls.append(minqty)
	
	ls.append(price)
	ls.append(image)
	print ls
	out.append(ls)

#initialize and open browser
br = init_driver()
br.get(url)
init_login(br,uname,passw)
time.sleep(1)

table = []

links = [i.get_attribute("href") for i in br.find_elements_by_css_selector("#global-header > table > tbody > tr:nth-child(2) > td.navleft-2012 > blockquote > p > a")]
cat = [i.text.encode("utf-8") for i in br.find_elements_by_css_selector("#global-header > table > tbody > tr:nth-child(2) > td.navleft-2012 > blockquote > p > a")]
pair = []

for x in range(len(links)-1):
	pr = []
	pr.append(links[x])
	pr.append(cat[x])
	pair.append(pr)
	
	
for pr in pair:
	if pr[0].split("/")[-1:] != "specials.html":
		print "Navigating to " + pr[0]
		br.get(pr[0])
		time.sleep(1)
		print "Showing all.."
		try:
			select = br.find_element_by_name("SortBy")
			opt = select.find_elements_by_tag_name("option")
			for op in opt:
				if op.text.encode("utf-8") == "Show All Products":
					op.click()
					time.sleep(1)
			item = [(i.text.encode("utf-8")).split()[1] for i in br.find_elements_by_css_selector("div.product-code")]
			for it in item:
				ls = []
				ls.append(it)
				ls.append(pr[1])
				print ls
				table.append(ls)
		except:
			print "Specials page detected."
			time.sleep(1)
	
outfile = open("./csv/outfile/pinecreek_catscraper_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)
br.close()           