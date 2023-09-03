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


login = "https://www.jonesrusticsigns.com/customer/account/login/"
url = "http://www.jonesrusticsigns.com/"
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
    
    driver.find_element_by_name("login[username]").send_keys(un)
    driver.find_element_by_name("login[password]").send_keys(pw)
    driver.find_element_by_name("send").click()
    time.sleep(5)
    print "Logged in."

def get_info(driver,link,out):
	driver.get(link)
	time.sleep(1)
	try:
		desc = driver.find_element_by_css_selector("div.std").text.encode("utf-8")
	except:
		desc = "No desc."
	desc2 = driver.find_element_by_css_selector("body > div > div > div.main-container.col2-right-layout > div > div.col-main > div.product-view > div.product-collateral > div > div").text.strip()
	try:
		cat = "|".join([i.text.encode("utf-8") for i in driver.find_elements_by_css_selector("div.breadcrumbs ul li")])
	except:
		cat = "No cat"
	try:
		image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#image"))).get_attribute("src")
	except:
		image = "No image."
	ls = []
	ls.append(desc2.split()[1:])
	ls.append(desc)
	ls.append(cat)
	ls.append(image)
	# try:
	opt = driver.find_elements_by_css_selector("#product-options-wrapper dl")
	for x in range(len(opt)):
		option = []
		term = driver.find_elements_by_css_selector("#product-options-wrapper dl")[x]
		option.append(term.find_element_by_css_selector("dt").text.encode("utf-8"))
		try:
			option.append("|".join([li.text.encode("utf-8") for li in term.find_elements_by_css_selector("dd ul li")]))
		except:
			option.append("|".join([li.get_attribute("href") for li in term.find_elements_by_css_selector("dd input")]))
		try:
			option.append("|".join([li.text.encode("utf-8") for li in term.find_elements_by_css_selector("dd select option")]))
		except:
			print "Values not detected."
		
		# try:
			# option.append("|".join([li.text.encode("utf-8") for li in term.find_elements_by_css_selector("dd > div ul li")]))
			# print "<li></li> option detected."
		# except:
			# try:
				# option.append("|".join([input.get_attribute("type") for input in term.find_elements_by_css_selector("dd > div > input")]))
				# print "<input> option detected."
			# except:
				# option.append("|".join([opt.text.encode("utf-8") for opt in term.find_elements_by_css_selector("dd > div > select option")]))
				# print "<option> option detected."
		ls.append(option)
	# except:
		# print "No option detected."
	print ls
	out.append(ls)


    
    
####################################################################################################################################################################################################################################
    
                
br = init_driver()
init_login(br,uname,passw)
time.sleep(1)

br.get(url)
print "Waiting for homepage to load..."
time.sleep(1)


items = []
table = []
cats = []

with open("./csv/infile/jonesrusticsigns.csv","rb") as infile:
    for i in infile:
		while True:
			try:
				br.find_element_by_name("q").clear()
				br.find_element_by_name("q").send_keys(i)
				time.sleep(1)
				break
			except:
				br.refresh()
				time.sleep(1)
				continue
		itm = [i.get_attribute("href") for i in br.find_elements_by_css_selector("h2.product-name a")]
		for i in itm:
			items.append(i)
			print i
		
for x in set(items):
	print x
	while True:
		try:
			get_info(br,x,table)
			time.sleep(1)
			break
		except Exception as e:
			print e
			br.refresh()
			time.sleep(3)
			continue

print "***Job Done***"
              
        
        
outfile = open("./csv/outfile/jonesrusticsigns_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)