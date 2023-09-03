import webdriver_config
from selenium.webdriver.common.keys import Keys
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

url = "http://pldthome.com/"
uname = "terence.galos@gmail.com"
passw = "malibuclub99"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

def init_login(driver,un,pw):
	driver.get(url)
	time.sleep(2)
	while True:
		try:
			driver.find_element_by_css_selector("a[href='https://my.pldthome.com']").click()
			time.sleep(2)
			break
		except:
			driver.refresh()
			continue
	WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#mySmartID"))).send_keys(un)
	driver.find_element_by_css_selector('#Password').send_keys(pw)
	driver.find_element_by_css_selector('#Password').send_keys(Keys.ENTER)
	print "Login Success."

def booster_viewer():
    acct = br.find_elements_by_css_selector("#account-list > li > div.account-info > b")
    for x in range(len(acct)):
        if br.find_elements_by_css_selector("#account-list > li > div.account-info > b")[x].text == "BroPostpaidLTE  ":
            br.find_elements_by_css_selector("#account-list > li > div.btn-holder > span:nth-child(1) > a")[x].click
            time.sleep(1)
            br.find_element_by_css_selector("#UsaDet > div > div.subDetails > div.pane > p > a").send_keys(Keys.PageDown)
            time.sleep(1)
	
#initialize and open browser
br = webdriver_config.init_driver()
br.maximize_window()
time.sleep(1)
init_login(br,uname,passw)
time.sleep(3)

booster_viewer()  