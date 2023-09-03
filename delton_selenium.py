
from selenium import webdriver
import time
import urllib
import requests
import csv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains
import os
import sys


login = "http://delton.cameoez.com/Scripts/PublicSite/?template=Login"
url = "http://delton.cameoez.com/Scripts/PublicSite/"
uname = "waresitat"
passw = "wolfville"




def init_driver():
	path = "./chrome_driver/chromedriver"
	browser = webdriver.Chrome(executable_path = path)
	browser.wait = WebDriverWait(browser,5)
	return browser
    
    
def init_login(driver,un,pw):
	print "Navigating to " + str(url) + " and logging in..."
	driver.get(login)
	print "Logging in."
	time.sleep(15)
	try:
		driver.find_element_by_name("username").send_keys(un)
		driver.find_element_by_name("password").send_keys(pw)
		driver.find_element_by_css_selector("#loginWrapper tbody tr:nth-child(2) td:nth-child(1) form table tbody tr:nth-child(3) td:nth-child(2) input[type=\"submit\"]").click()
		time.sleep(1)
		print "Logged in."
	except:
		print "Log in failed."
		driver.close()
        
def get_info(driver,link,out):

    driver.get(link)
    time.sleep(1)
    name = driver.find_element_by_id("item-contenttitle")
    sku = driver.find_element_by_css_selector("div.code em")
    cat = driver.find_element_by_css_selector("div.breadcrumbs")
    desc = driver.find_element_by_id("caption")
    
    try:
        vary = driver.find_elements_by_tag_name("option")
    except:
        vary = "none"
    
    try:
		image = driver.find_element_by_css_selector("img.image-l")
		driver.get(image)
		time.sleep(1)
		driver.save_screenshot(image.split("/")[-1:][0])
    except:
        image = "none"
    
    try:
        for i in vary:
            ls = []
            ls.append(name.text.encode("utf-8"))
            ls.append(i.text.encode("utf-8"))
            ls.append(sku.text.encode("utf-8"))
            ls.append(cat.text.encode("utf-8"))
            ls.append(desc.text.encode("utf-8"))
            try:
                ls.append(image.get_attribute("src"))
            except:
                ls.append(image)
            print ls
            out.append(ls)
    except:
        ls = []
        ls.append(name.text.encode("utf-8"))
        ls.append(vary)
        ls.append(sku.text.encode("utf-8"))
        ls.append(cat.text.encode("utf-8"))
        ls.append(desc.text.encode("utf-8"))
        try:
            ls.append(image.get_attribute("src"))
        except:
            ls.append(image)
        print ls
        out.append(ls)        
        

        
###################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
        
		
category = []
items = []
table = []


br = init_driver()
init_login(br,uname,passw)
time.sleep(1)

with open("./csv/infile/delton_infile.csv","rb") as infile:
    for i in infile:
        while True:
            try:
                br.find_element_by_name("term").clear()
                br.find_element_by_name("term").send_keys(i)
                time.sleep(1)
                break
            except:
                br.refresh()
                time.sleep(1)
                continue
        try:
			ls = []
			link = br.find_element_by_css_selector("a.popup.cboxElement").get_attribute("href")
			br.get(link)
			time.sleep(1)
			image = br.find_element_by_css_selector("#imgCell > img").get_attribute("src")
			sku = br.find_element_by_css_selector("#descCell > p.sku").text.encode("utf-8")
            
			ls.append(sku.split(" ")[1])
			ls.append(image.strip())
			print ls
			table.append(ls)
			br.back()
			time.sleep(1)
			# url = "E:\rick stuart images\delton\New folder (3)"
			# br.save_screenshot(image.split("/")[-1:][0])
			
			#download pics to desired directory
			name = image.split("/")[-1:][0]
			curdir = os.getcwd()
			path = curdir + "\\images\\delton\\" + name
			print path
			# path = r'E:\rick stuart images\delton\New folder (3)' + "\\" + name
			# print path
			try:
				urllib.urlretrieve(image,path)
				time.sleep(1)
			except Exception as e:
				print e
			br.back()
			time.sleep(1)
        except:
            print "Item not found."
            # print i
            # br.get(i)
            # time.sleep(1)
            # name = i.split("/")[-1:]
            # print name
            # curdir = os.getcwd()
            # path = curdir + "\\images\\delton\\" + str(name[0].strip())
            # print path
            # time.sleep(1)
            
            # urllib.urlretrieve(i,path)
            
        # try:
			# ls = []
			# desc = br.find_element_by_css_selector("#product div span").text.encode("utf-8")
			# spl = desc.splitlines()
			# ls.append(spl[len(spl)-1])
			# ls.append(spl[len(spl)-2])
			# print ls
			# table.append(ls)
		# except:
			# print "Item not found."
			
outfile = open("./csv/outfile/delton_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"        
   