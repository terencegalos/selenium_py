import webdriver_config
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

url = "http://warmglow.com/"
uname = "rick@waresitat.com"
passw = "wolfville"
count = 0

    
def init_login(driver,un,pw):
    driver.get(url)
    time.sleep(120)
    br.find_element_by_css_selector("#sw_dropdown_778 a").click()
    time.sleep(3)
    br.find_element_by_css_selector("#account_info_778 div.ty-account-info__buttons.buttons-container a.ty-btn.ty-btn__primary").click()
    time.sleep(2)
    print "Logging in."
    try:
        driver.find_element_by_id("login_main_login").send_keys(un)
        driver.find_element_by_id("psw_main_login").send_keys(pw)
        time.sleep(8)
        driver.find_element_by_name("dispatch[auth.login]").click()
        time.sleep(5)
        print "Logged in."
    except:
        print "Log in failed."
        driver.close()

def get_info(br,out):
	items = br.find_elements_by_css_selector("div.item-holder")
	print items
	
	for item in items:
		ls = []
		try:
			ls.append(item.find_element_by_css_selector("h3").text.encode("utf-8"))
			ls.append(item.find_element_by_css_selector("img.product-loop-image").get_attribute("src"))
			print ls
			out.append(ls)
		except Exception as e:
			print e
			time.sleep(3)

br = webdriver_config.init_driver()
while True:
	try:
		br.get(url)
		time.sleep(1)
		break
	except Exception as e:
		print e
		br.refresh()
		time.sleep(1)
		continue

table = []
items = []

ActionChains(br).move_to_element(br.find_element_by_css_selector("a.menu-item-link")).perform()
time.sleep(1)
itemlinks = [i.get_attribute("href") for i in br.find_elements_by_css_selector("a.menu-item-link")]
print itemlinks

for link in itemlinks:
    print "Status:Navigating to " + link
    while True:
		try:
			br.get(link)
			time.sleep(1)
			break
		except Exception as e:
			if count > 3: # count number of tries
				count = 0
				get_info(br,table)
			print e
			time.sleep(1)
			count = count + 1
			continue
    get_info(br,table)


print "***Job Done***"        


        
outfile = open("./csv/outfile/warmglow_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)