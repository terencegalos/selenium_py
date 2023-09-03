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

def vendor_file(v):
	files = os.listdir(".")
	for file in files:
		if v in file.lower():
			return file
def all_images():
	cur = os.getcwd()
	# print cur
	return "\n".join([cur+"\\"+file for file in os.listdir(".")])

def go_to_shst():

	dir = os.getcwd()
	
	if dir == "C:\\Users\\Berries\\Code":
		dest = "C:\Dropbox\SHST Files\RETAIL SHEET SHST\\"
	else:
		dest = "F:/Dropbox/SHST Files/RETAIL SHEET SHST/"
	os.chdir(dest)
	
	# all = [path for path in os.listdir(".") if os.path.isdir(path)]
	# latest = max(all,key = os.path.getmtime)
	# os.chdir(latest+"/800/")
	# os.chdir(latest)
	print os.getcwd()
	return dest
	
	# return dest+latest
	
def upload(infile):
	try:
		# br.find_element_by_css_selector("body > div > section.header_section > div > div > div.col-lg-9.col-sm-12.col-md-9 > div > ul > li.dropdownList.menu-dropdown-icon > ul > div > li:nth-child(1) > ul > li:nth-child(3) > a").click()
		WebDriverWait(br,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div > section > div > div > div.col-lg-9.col-sm-12.col-md-9 > div > ul > li.dropdownList.menu-dropdown-icon > ul > div > li:nth-child(2) > ul > li > a"))).click()
	except:
		time.sleep(1)
		pass
	# time.sleep(1)
	dir = go_to_shst()
	time.sleep(5)
	# print all_img
	# while True:
		# try:
	print "Uploading..."
	br.find_element_by_css_selector("body > div > div:nth-child(11) > div > div > fieldset > legend > div.pull-right > span:nth-child(3) > a").click()
	time.sleep(1)
	btn = WebDriverWait(br,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div > div:nth-child(11) > div > div > fieldset > form > div:nth-child(5) > div:nth-child(1) > input")))
	br.execute_script("window.stop();")
	btn.send_keys(dir+vendor_file(vendor.split()[0].lower()))
	btn.submit()
	print "Vendor upload success."
			# break
		# except:
			# time.sleep(1)
			# br.execute_script("window.stop();")
			# continue
	
	

def con():
	rbook = xlrd.open_workbook("./csv/outfile/Brands SHST Master sheet.xls")
	rsheet = rbook.sheet_by_index(0)
	for x in range(rsheet.nrows):
		row = rsheet.row(x)
		if row[0].value == vendor:
			print row[0].value
			return [row[1].value,row[2].value,row[4].value]
	

def login(un,pw):
	print "Logging in"
	# WebDriverWait(br,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div > section.header_section > div > div > div.col-lg-9.col-sm-12.col-md-9 > div > ul > li.dropdownList.menu-dropdown-icon > a"))).click()
	# WebDriverWait(br,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div > section.header_section > div > div > div.col-lg-9.col-sm-12.col-md-9 > div.menu > ul > li.dropdownList.hidden-xs"))).click()
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
	uname,passw,infile = con()
	login(uname,passw)
	upload(infile)
	
	
if __name__ == "__main__":
	main()
