import time
import csv
import os, sys, shutil,xlrd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import webdriver_config as driver

vendor = sys.argv[1]


br = driver.init_driver()

def all_images():
	cur = os.getcwd()
	# print cur
	return "\n".join([cur+"\\"+file for file in os.listdir(".")])

def go_last_mod_dir():

	dir = os.getcwd()
	
	if dir == "C:\\Users\\Berries\\Code":
		dest = "D:\\Waresitat Images\\" + vendor + "\\"
	else:
		dest = "D:\\Rick\\" + vendor + "\\"
	os.chdir(dest)
	
	all = [path for path in os.listdir(".") if os.path.isdir(path)]
	latest = max(all,key = os.path.getmtime)
	os.chdir(latest)
	print os.getcwd()
	
	return dest+latest
	
def upload():
	try:
		# br.find_element_by_css_selector("body > div > section.header_section > div > div > div.col-lg-9.col-sm-12.col-md-9 > div > ul > li.dropdownList.menu-dropdown-icon > ul > div > li:nth-child(1) > ul > li:nth-child(3) > a").click()
		WebDriverWait(br,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div > section.header_section > div > div > div.col-lg-9.col-sm-12.col-md-9 > div > ul > li.dropdownList.menu-dropdown-icon > ul > div > li:nth-child(1) > ul > li:nth-child(3) > a"))).click()
	except:
		time.sleep(1)
		pass
	# time.sleep(1)
	dir = go_last_mod_dir()
	all_img = all_images()
	print all_img
	while True:
		try:
			print "Uploading..."
			# btn = br.find_element_by_css_selector("#filesContainer > input")
			btn = WebDriverWait(br,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#filesContainer > input")))
			# br.execute_script("window.stop();")
			btn.send_keys(all_img)
			btn.submit()
			print "Image upload success."
			break
		except:
			time.sleep(1)
			continue
	
	

def authenticate():
	rbook = xlrd.open_workbook("./csv/outfile/Brands SHST Master sheet.xls")
	rsheet = rbook.sheet_by_index(0)
	for x in range(rsheet.nrows):
		row = rsheet.row(x)
		if row[0].value == vendor:
			print row[0].value
			return [row[1].value,row[2].value]
	

def login(un,pw):
	print "Logging in"
	# br.find_element_by_css_selector("body > div > section.header_section > div > div > div.col-lg-9.col-sm-12.col-md-9 > div > ul > li.dropdownList.menu-dropdown-icon > a").click()
	# WebDriverWait(br,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a.signIN_menu"))).click()
	time.sleep(1)
	br.find_element_by_name("email").send_keys(un)
	br.find_element_by_name("password").send_keys(pw)
	br.find_element_by_name("password").send_keys(Keys.ENTER)
	time.sleep(1)
	print "Accessed."

def main():

	url = "https://www.shophereshopthere.com/"
	
	uname = ""
	passw = ""

	br.get(url)
	time.sleep(1)
	uname,passw = authenticate()
	login(uname,passw)
	upload()
	
	
if __name__ == "__main__":
	main()
