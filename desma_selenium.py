
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
url = "http://desma-group.com/home-decor/wall-decor.html"
uname = "rick@waresitat.com"
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
    
def init_login(driver,un,pw):
    driver.get(login)
    print "Logging in."
    try:
        driver.find_element_by_name("login[username]").send_keys(un)
        driver.find_element_by_name("login[password]").send_keys(pw)
        driver.find_element_by_name("send").click()
        time.sleep(5)
        print "Logged in."
    except:
        print "Log in failed."         
        
        
def get_info(driver,link,out):
	driver.get(link)
	time.sleep(1)
	sku = driver.find_element_by_css_selector("p.product_title").text.encode("utf-8")
	cat = driver.find_element_by_css_selector("div.breadcrumb").text.encode("utf-8")
	desc = driver.find_element_by_css_selector("div.summary").text.encode("utf-8")
	infos = driver.find_elements_by_css_selector("#product-attribute-specs-table tbody tr")
	inf = []
	try:
		for info in infos:
			inf.append("|".join([i.text.encode("utf-8") for i in info.find_elements_by_css_selector("td")]))
	except:
		inf = "No info."
	try:
		vary = [i.text.encode("utf-8") for i in driver.find_elements_by_css_selector("option")]
	except:
		vary = "No option."
	try:
		image = driver.find_element_by_css_selector("img.productimg").get_attribute("src")
	except:
		image = "No pic."
	# try:
		# for i in vary:
			# ls = []
			# ls.append(i)
			# ls.append(sku)
			# ls.append(cat)
			# ls.append(desc)
			# ls.append("i".join(inf))
			# ls.append(image)
			# print ls
			# out.append(ls)
	# except:
	ls = []
	ls.append(sku)
	ls.append(cat)
	ls.append(desc)
	ls.append("i".join(inf))
	ls.append(image)
	print ls
	out.append(ls)        

br = init_driver()
# br.get(url)
init_login(br,uname,passw)
# time.sleep(1)
# br.get(url)
time.sleep(1)


items = []
table = []

# sections = br.find_elements_by_css_selector("dd a")
# sectionlinks = []

# for link in sections:
    # sectionlinks.append(link.get_attribute("href"))
    # print link.get_attribute("href")

# sectionlinks.append("http://desma-group.com/inspirational.html")
# sectionlinks.append("http://desma-group.com/home-decor.html")
# sectionlinks.append("http://desma-group.com/gifts.html")
# sectionlinks.append("http://desma-group.com/seasonal.html")
# sectionlinks.append("http://desma-group.com/others.html")

    
# for i in sectionlinks:
    # print i
    # br.get(i)
    # time.sleep(1)
    # try:
        # page = br.find_element_by_css_selector("b.number").text.split()
    # except:
        # print "No item found in this section."
    # print page[0]
    # itemperpage = int(page[0])/12
    # print itemperpage
    # item = br.find_elements_by_css_selector("p.title a")
    # for i in item:
        # items.append(i.get_attribute("href"))
        # print i.get_attribute("href")
    # for x in range(itemperpage):
        # try:
            # br.find_element_by_css_selector("a.next").click()
            # time.sleep(1)
            # item = br.find_elements_by_css_selector("p.title a")
            # for i in item:
                # items.append(i.get_attribute("href"))
                # print i.get_attribute("href")
        # except:
            # print "No more next page..."
            
# outfile1= open("./csv/outfile/desma_items4.csv","wb")
# writer1 = csv.writer(outfile1)
# writer1.writerow(items)            

# ulist = list(set(items))            

# for item in ulist:
    # try:
        # ls = []
        # br.get(item)
        # time.sleep(1)
        # desc = br.find_element_by_css_selector("div.summary").text.encode("utf-8")
        # sku = br.find_element_by_css_selector("#product-attribute-specs-table tbody tr.first.odd td.data.last").text.encode("utf-8")
        # cat = br.find_element_by_css_selector("div.breadcrumb").text.encode("utf-8")
        # try:
            # image = br.find_element_by_css_selector("#product_addtocart_form div.product_image div ul li a").get_attribute("onclick")
        # except:
            # image = "none"
        # dim = br.find_element_by_css_selector("#product-attribute-specs-table tbody tr.even td.data.last").text.encode("utf-8")
        # qty = br.find_element_by_id("qty").get_attribute("value")
        # price = br.find_element_by_css_selector("span.price").text.encode("utf-8")

        # ls.append(desc)
        # ls.append(sku)
        # ls.append(cat)
        # ls.append(dim)
        # ls.append(qty)
        # ls.append(price)
        # ls.append(image)
        # table.append(ls)
        # print ls 
    # except:
        # print "Some error occured."

with open("./csv/infile/desma.csv","rb") as infile:
	for i in infile:
		print "Searching for item " + str(i)
		ActionChains(br).move_to_element(br.find_element_by_name("q")).perform()
		time.sleep(1)
		br.find_element_by_name("q").clear()
		br.find_element_by_name("q").send_keys(i)
		time.sleep(1)
		# try:
		items = [it.get_attribute("href") for it in br.find_elements_by_css_selector("ul.productlist li a")]
		for i in items:
			get_info(br,i,table)
		# except Exception as e:
			# print e
			# time.sleep(1)
			# print "Item not found."
        
                
        
outfile = open("./csv/outfile/desma_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"        
   