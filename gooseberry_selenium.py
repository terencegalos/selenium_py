from selenium import webdriver
import time
import urllib
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from urllib2 import urlopen
import csv

pages = ["http://www.yourheartsdelight.com/c-152-autumn-welcome.aspx?pagesize=96","http://www.yourheartsdelight.com/c-401-fall-fun.aspx","http://www.yourheartsdelight.com/c-1274-pumpkin-patch-pals.aspx","http://www.yourheartsdelight.com/c-1355-branches.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1378-candle-rings.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1357-collections.aspx","http://www.yourheartsdelight.com/c-1386-premade.aspx","http://www.yourheartsdelight.com/c-1349-picks.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1367-garlands.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1348-wreaths.aspx?pagesize=96","http://www.yourheartsdelight.com/c-593-boxes.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1272-burlap-ornaments.aspx?pagesize=96","http://www.yourheartsdelight.com/c-598-candles-lights-accessories.aspx?pagesize=96","http://www.yourheartsdelight.com/c-180-containers.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1165-decorative-plates-bowls.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1165-decorative-plates-bowls.aspx?pagesize=96","http://www.yourheartsdelight.com/c-363-dolls.aspx?pagesize=96","http://www.yourheartsdelight.com/c-637-fall-accents.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1164-frames-wall-decor.aspx?pagesize=96","http://www.yourheartsdelight.com/c-600-home-fragrance.aspx","http://www.yourheartsdelight.com/c-402-magnets.aspx","http://www.yourheartsdelight.com/c-362-ornaments.aspx","http://www.yourheartsdelight.com/c-1192-outdoor-decor.aspx","http://www.yourheartsdelight.com/c-400-pins.aspx","http://www.yourheartsdelight.com/c-82-pumpkins.aspx?pagesize=96","http://www.yourheartsdelight.com/c-616-runners-mats.aspx?pagesize=96","http://www.yourheartsdelight.com/c-364-scarecrows.aspx?pagesize=96","http://www.yourheartsdelight.com/c-708-tableware.aspx?pagesize=96","http://www.yourheartsdelight.com/c-1177-thanksgiving.aspx?pagesize=96","http://www.yourheartsdelight.com/c-804-twigs.aspx?pagesize=96"]
uname = "service@waresitat.com"
pw = "wolfville"
url = "http://www.gooseberrypatch.com/"

def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]
    
def get_info(driver,link,out,sku):
    ls = []
    print link
    driver.get(link)
    
    time.sleep(1)
    # sku = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.sku"))).text.encode("utf-8")
    # cat = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.SectionTitleText"))).text.encode("utf-8")
    name = driver.find_element_by_css_selector("#site-body > div.row.padded-h > div > header > div > div > div > div:nth-child(1) > h1").text.encode("utf-8")
    cat = "|".join([i.text.encode("utf-8") for i in driver.find_elements_by_css_selector("#page-header-actions > ul > li > span")])
    image = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content-wrap > div > div > article > div > div:nth-child(1) > div > div > a > img"))).get_attribute("src")
    ls.append(name)
    ls.append(sku)
    ls.append(cat)
    ls.append(image)
    print ls
    out.append(ls)
    
#initialize and open browser
br = init_driver()
br.get(url)

# br.find_element_by_id("ctl00_PageContent_EMail").send_keys(uname)
# br.find_element_by_id("ctl00_PageContent_txtPassword").send_keys(pw)
# br.find_element_by_id("ctl00_PageContent_LoginButton").click()
time.sleep(1)

table = []

with open("./csv/infile/gooseberry.csv","rb") as infile:
	for it in infile:
		print str(it)   
		br.get(url)
		time.sleep(1)
		while True:
			try:
				br.find_element_by_name("globalkeyword").clear()
				br.find_element_by_name("globalkeyword").send_keys(str(it))
				break
			except:
				br.refresh()
				time.sleep(1)
				continue
		time.sleep(1)
		try:
			br.find_element_by_css_selector("#results > table > tbody > tr:nth-child(2) > td > p > b > a").click()
			time.sleep(1)
			ls = []
			name = br.find_element_by_css_selector("table:nth-child(2) > tbody > tr > td:nth-child(3) > font:nth-child(1) > strong").text.encode("utf-8")
			cat = "|".join([i.text.encode("utf-8") for i in br.find_elements_by_css_selector("b.breadcrumb a")])
			image = br.find_element_by_css_selector("#monGroup0 > a:nth-child(5) > img").get_attribute("src"	)
			ls.append(name)
			ls.append(it)
			ls.append(cat)
			ls.append(image.replace("50x50","1000x1000"))
			print ls
			table.append(ls)
		except:
			print "Item not found."
         
    

outfile = open('./csv/outfile/gooseberry_output.csv','wb')
writer = csv.writer(outfile)
writer.writerows(table)

print "Job done. Closing browser."
br.close()