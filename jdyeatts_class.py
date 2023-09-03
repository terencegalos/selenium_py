from selenium.webdriver.common.keys import Keys
from table_gateway import gateway
import domainobject
from selenium.webdriver.common.action_chains import ActionChains

class jdyeatts(domainobject.domainobject):

    vendor = "Chesapeake Bay & JD Yeatts"
    url = "https://www.jdyeatts.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    login = "https://www.jdyeatts.com/"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(2)
        
        print "Logging in."
        self.driver.find_element_by_name("LOG_ID").send_keys(un)
        self.driver.find_element_by_name("LOG_ID").send_keys(Keys.TAB)
        # self.driver.find_element_by_name("LOG_ID").click()
        self.time.sleep(1)
        self.driver.find_element_by_id("password").send_keys(pw)
        self.driver.find_element_by_id("password").send_keys(Keys.ENTER)
        self.time.sleep(3)
        print "Success."

    def get_info(self,item=None):
		db = gateway()
		db.name = self.driver.find_element_by_css_selector("body > div > div.product-header > div.product-title").text.encode("utf-8")
		db.sku = self.driver.find_element_by_css_selector("body > div > div.product-info > table > tbody > tr:nth-child(1) > td:nth-child(3)").text.splitlines()[0].split()[1]
		db.cat = item
		db.desc = self.driver.find_element_by_css_selector("body > div > div.product-description").text.encode("utf-8")
		try:
			db.stock = self.driver.find_element_by_css_selector("body > div > div.product-info > table > tbody > tr > td > span.instock").text.encode("utf-8")
		except:
			db.stock = self.driver.find_element_by_css_selector("body > div > div.product-info > table > tbody > tr:nth-child(2) > td:nth-child(1) > span.outstock").text.encode("utf-8")
		db.sale = ""
		db.set = ""
		db.custom = ""
		db.size = ""
		db.seller = ""
		db.min1 = self.driver.find_element_by_css_selector("body > div > div.product-info > table > tbody > tr:nth-child(3) > td.p-levels > div:nth-child(1)").text.split()[0]
		db.price1 = self.driver.find_element_by_css_selector("body > div > div.product-info > table > tbody > tr:nth-child(3) > td.p-levels > div:nth-child(2)").text.split()[-2]
		db.min2 = self.driver.find_element_by_css_selector("body > div > div.product-info > table > tbody > tr:nth-child(3) > td.p-levels > div:nth-child(3)").text.split()[0]
		db.price2 = self.driver.find_element_by_css_selector("body > div > div.product-info > table > tbody > tr:nth-child(3) > td.p-levels > div:nth-child(4)").text.split()[-2]
		db.min3 = self.driver.find_element_by_css_selector("body > div > div.product-info > table > tbody > tr:nth-child(3) > td.p-levels > div:nth-child(5)").text.split()[0]
		db.price3 = self.driver.find_element_by_css_selector("body > div > div.product-info > table > tbody > tr:nth-child(3) > td.p-levels > div:nth-child(6) > span").text.split()[-2]
		db.multi = ""
		db.dir400 = "JDYEATTS400"
		db.dir160 = "JDYEATTS160"
		try:
			db.img400 = self.driver.find_element_by_css_selector("#large_picture").get_attribute("src")
		except:
			print "Image not found."
			return
		db.img160 = db.img400.split("/")[-1:][0]
		db.desc2 = ""
		db.option = ""
		db.dir800 = "JDYEATTS800"
		db.img800 = db.img160
		# self.driver.switch_to.default_content()
		self.driver.back()
		self.time.sleep(1)
		print db
		return db
        
        
    def search_item(self,row):
			print "\nSearching for item: " + row+"\n"
			
			try:
				self.driver.find_element_by_name("I_PROD_DESC").clear()
			except:
				self.driver.switch_to.default_content()
				self.driver.find_element_by_name("I_PROD_DESC").clear()
				
			self.driver.find_element_by_name("I_PROD_DESC").send_keys(str(row))
			self.driver.find_element_by_name("I_PROD_DESC").send_keys(self.Keys.ENTER)
			self.time.sleep(1)
			
			# self.driver.execute_script("return document.querySelector('body > div.wrapper > div.main-content > div:nth-child(2) > iframe').contentWindow.document.body.querySelector('div.product a')").click()
			try:
				iframe = self.driver.find_element_by_css_selector("body > div.wrapper > div.main-content > div:nth-child(2) > iframe")
				self.driver.switch_to.frame(iframe)
				self.time.sleep(1)
				self.driver.find_element_by_css_selector("div.product a").click()
				self.time.sleep(1)
			except:
				return None

