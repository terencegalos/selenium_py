from table_gateway import gateway
from bs4 import BeautifulSoup as bs
import domainobject
import requests,xmltodict
import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class northlight(domainobject.domainobject):

    vendor = "Northlight Seasonal"
    url = "http://northlightseasonal.com/"
    home = "http://northlightseasonal.com/"
    sitemap1 = "https://northlightseasonal.com/sitemap_products_1.xml?from=5568011459&to=988096856108"
    sitemap2 = "https://northlightseasonal.com/sitemap_products_2.xml?from=988096888876&to=43132015 08454"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    links = []
    
    def init_xml(self):
        map1 = requests.get(self.sitemap1)
        self.time.sleep(1)
        map2 = requests.get(self.sitemap2)
        self.time.sleep(1)

        data1 = xmltodict.parse(map1.content)
        print data1
        self.time.sleep(1)
        data2 = xmltodict.parse(map2.content)
        print data2
        self.time.sleep(1)

        self.links.extend([d['loc'] for d in data1['urlset']['url'] if d['loc'] not in self.links])
        self.links.extend([d['loc'] for d in data2['urlset']['url'] if d['loc'] not in self.links])
        print len(self.links)
        self.time.sleep(10)


    def init_login(self,un,pw):
		self.driver.get(self.url)
		self.time.sleep(3)
		#while True:
			#self.driver.find_element_by_css_selector("#privy-inner-container > div:nth-child(1) > div > div.privy-popup-inner-content-wrap > div.privy-dismiss-content > div").click()
			#break
		#self.time.sleep(1)
		while True:
			self.driver.get("https://northlightseasonal.com/account/login")
			break
		self.time.sleep(1)
		print "Logging in..."
		self.driver.find_element_by_name("customer[email]").send_keys(un)
		self.driver.find_element_by_name("customer[password]").send_keys(pw)
		self.driver.find_element_by_name("customer[password]").send_keys(Keys.ENTER)
		print "Success."

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = (self.driver.find_element_by_css_selector("#content > h1").text.encode("utf-8")).replace(",","/comma")
        except:
            return
        # db.sku = (self.driver.find_element_by_css_selector("#content > div.productdetail > div.description.pagecontent.simple").text.split("SKU:")[1])
        db.sku = [line for line in self.driver.find_element_by_css_selector("#content > div.productdetail > div.description.pagecontent.simple").text.encode("utf-8").splitlines() if "SKU" in line][0]
        #db.cat = self.driver.find_element_by_css_selector("#breadcrumbs").get_attribute("innerHTML").splitlines() #"|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("#breadcrumbs > span > a")])
        htmNode = self.driver.find_element_by_css_selector("#breadcrumbs").get_attribute("innerHTML") #"|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("#breadcrumbs > span > a")])
        # print "***"
        # print htmNode
        # print "***"
        txt =  re.search(r'<div class="socitem">(\n*|.*|\s*|\w*)*</div>"*',htmNode).group()
        soup = bs(txt)
        db.cat = soup.find('a')['href'].split("&")[-2] #re.match(r'<div class=\"socitem\">(.*?|\n*?|\s*?)*</div>',htmNode)
        db.desc = self.driver.find_element_by_css_selector("#content > div.productdetail > div.description.pagecontent.simple").text.encode("utf-8")
        try:
            db.stock = self.driver.find_element_by_css_selector("#product-form").text.splitlines()[-2]
        except:
            db.stock = ""

        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
            db.min1 = self.driver.find_element_by_css_selector("#product-form > div.quantity > input[type=text]").get_attribute("value")
        except:
            db.min = 1

        try:
            db.price1 = self.driver.find_element_by_css_selector("#price-field").text.strip()
        except:
            db.price1 = 999.99
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "northlight400"
        db.dir160 = "northlight160"
        try:
            db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.main a"))).get_attribute("href")
        except:
            db.img400 = "No image."
        db.img160 = (db.img400.split("/")[-1:][0]).split("?")[0] if ".jpg?" in db.img400 else ""
        db.desc2 = ""
        db.option = ""
        db.dir800 = "northlight800"
        db.img800 = db.img160
        # print db
        print db.cat
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        #while True:
            #try:
        self.driver.find_element_by_name("q").clear()
        self.driver.find_element_by_name("q").send_keys(" ".join(row.split("_")))
        self.driver.find_element_by_name("q").send_keys(Keys.ENTER)
        self.time.sleep(1)
                #break
            #except:
             #   self.driver.refresh()
              #  continue
        
        try:
            item = self.driver.find_element_by_css_selector("ol.searchresults li h3 a").get_attribute("href")
            print item
            return [item]
        except Exception as e:
            print e
            return None
