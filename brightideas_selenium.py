from selenium.webdriver.support.ui import Select
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
from bs4 import BeautifulSoup

login = "http://delton.cameoez.com/Scripts/PublicSite/?template=Login"
url = "https://www.brightideasllc.com/index.php"
uname = "rick@waresitat.com"
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
    
def init_login(driver,un,pw):
    print "Navigating to " + str(url) + " and logging in..."
    print "Logging in."
    try:
		driver.find_element_by_name("username").send_keys(un)
		driver.find_element_by_name("password").send_keys(pw)
		driver.find_element_by_css_selector("#content-box table tbody tr td:nth-child(1) form p input[type=\"image\"]:nth-child(8)").click()
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
br.get(url)
init_login(br,uname,passw)
time.sleep(2)

# menu = br.find_elements_by_css_selector("#login div a.menuitem.submenuheader")


# #main menu

# for x in range(1,len(menu)):
	# print menu[x].get_attribute("innerHTML")
	# print "\n"
	# menu[x].click()
	# time.sleep(1)
	# #submenu
subm = br.find_elements_by_css_selector("#login div div.submenu ul li a")

cats = []
submenu = []

for su in subm:
	submenu.append(su.get_attribute("href"))
	cats.append(su.get_attribute("innerHTML"))
	
for sub in range(4,len(submenu)):
	print submenu[sub]
	br.get(submenu[sub])
	time.sleep(1)
	
	#show all
	br.find_element_by_link_text("Show All").click()
	print "Showing all items.."
	time.sleep(2)
	
	#pageitems
	cat = cats[sub]
	items = br.find_elements_by_css_selector("#product table tbody tr")
	
	for item in items:
		ls = []
		try:
			pic = item.find_element_by_css_selector("td:nth-child(1) a span img").get_attribute("src")
			desc = item.find_element_by_css_selector("td:nth-child(2)").text.encode("utf-8")
			pricebreaks = item.find_element_by_css_selector("td:nth-child(3)").text.encode("utf-8")
			description = desc.splitlines()
			print "\n"
			
			ls.append(description)
			ls.append(cat)
			ls.append(pricebreaks)
			ls.append(pic)
			
			print ls
			table.append(ls)
		except:
			print "Skipped."
			
outfile = open("./csv/outfile/brightideasllc_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"        
   