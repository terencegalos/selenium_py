from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class impressions(domainobject.domainobject):

    vendor = "Impressions on Market"
    search = "http://www.impressionsonmarket.com/search-general"
    url = "http://www.impressionsonmarket.com/"
    home = "http://www.impressionsonmarket.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        # self.driver.find_element_by_css_selector("#site > header > div > div > div.navigation > div > nav > ul:nth-child(2) > li:nth-child(3) > a").click()
        # self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_css_selector("body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > modal > div.modal-body > modal-body > div.row.m-a-3 > div > login-fieldset > div:nth-child(1) > div > div > div:nth-child(1) > div > input").send_keys(un)
        # self.driver.find_element_by_css_selector("body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > modal > div.modal-body > modal-body > div.row.m-a-3 > div > login-fieldset > div:nth-child(2) > div > div > div:nth-child(1) > div > input").send_keys(pw)
        # self.driver.find_element_by_css_selector("body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > modal > div.modal-body > modal-body > div.row.m-a-3 > div > login-fieldset > div:nth-child(2) > div > div > div:nth-child(1) > div > input").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
		db = gateway()
		try:
			db.name = self.driver.find_element_by_css_selector("li.productItem > div > div:nth-child(2) > h3").text.encode("utf-8")
		except:
			return
		db.sku = self.driver.find_element_by_css_selector("li.productItem > div > div:nth-child(1) > div.image-large").text.encode("utf-8")
		db.cat = ""
		db.desc = self.driver.find_element_by_css_selector("li.productItem > div > div:nth-child(2) > div.description").text.encode("utf-8")
		db.stock = ""
		db.sale = ""
		db.set = ""
		db.custom = self.driver.current_url
		db.size = ""
		db.seller = ""
		db.min1 = ""
		db.price1 = ""
		db.min2 = ""
		db.price2 = ""
		db.min3 = ""
		db.price3 = ""
		db.multi = ""
		db.dir400 = "Impressions400"
		db.dir160 = "Impressions160"
		try:
			db.img400 = self.driver.find_element_by_css_selector("li.productItem > div > div:nth-child(1) > div.image-large > img").get_attribute("src")
		except Exception as e:
			print e
			self.time.sleep(3)
			return
		db.img160 = db.img400.split("/")[-1:][0]
		db.desc2 = ""
		try:
			db.option = "|".join([o.text.encode("utf-8") for o in self.driver.find_elements_by_css_selector("div.productAttributes > div > div.catProdAttributeItem > select option")])
		except:
			db.option = ""
		db.dir800 = "Impressions800"
		db.img800 = db.img160
		print db
		return db
        
        
    def search_item(self,row):
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.get("http://www.impressionsonmarket.com/search-general")
                self.time.sleep(01)
                self.driver.find_element_by_name("CAT_Search").send_keys(str(row))
                self.driver.find_element_by_name("CAT_Search").send_keys(Keys.ENTER)
                self.time.sleep(self.delay)
                break
            except:
                self.driver.get(self.url)
                self.time.sleep(self.delay)
                continue

        try:
            item = self.driver.find_element_by_css_selector("div.search-results > div > h3 > a").get_attribute("href")
            print item
            return [item]
        except:
            return None

