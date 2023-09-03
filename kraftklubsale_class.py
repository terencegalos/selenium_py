from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class kraftklubsale(domainobject.domainobject):

    vendor = "Kraft Klub"
    url = "http://kraftklub.com/myaccount.php"
    login = "https://kraftklub.com/customer/login"
    home = "http://kraftklub.com/index.html"
    uname = "kaye.williams@waresitat.com"
    passw = "b2bonline"
    delay = 1
    links = []
    
    def init_login(self,un,pw):
        self.driver.get(self.login)
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("email").send_keys(un)
        self.driver.find_element_by_name("password").send_keys(pw)
        resp = True
        while resp:
			
			inp = raw_input("Ready?")
			if inp.lower() == "yes":
				resp = False

			self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
			self.time.sleep(1)
			print "Success."
        
    def nextPage(self):
		try:
			self.driver.find_element_by_link_text("Next").click()
			self.time.sleep(1)
			return True
		except:
			print "Page exhausted."
			return False

    def get_links(self):
		items = [l.get_attribute("href") for l in self.driver.find_elements_by_css_selector("#right > div:nth-child(2) > div > div.pic > a")]
		print items
		return items

    def get_all_items(self):
		self.driver.find_element_by_css_selector("#nav_15").click()
		self.time.sleep(1)

		cats = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#leftside > div.menubox > li > a")]
		for cat in cats:
			self.driver.get(cat)
			self.time.sleep(1)
			self.links.extend(self.get_links())


    def get_info(self,item=None):
		db = gateway()
		# db.name = ""
		db.name = self.driver.find_element_by_css_selector("#product-form > div > div.right.col-lg-7 > div.row.info > h2:nth-child(2)").text
		db.sku = self.driver.find_element_by_css_selector("#product-form > div > div.right.col-lg-7 > div.row.info > h2:nth-child(1)").text.split()[0]
		db.cat = "|".join([c.text.encode("utf-8") for c in self.driver.find_elements_by_css_selector("#location > a")])

		try:
			db.desc = self.driver.find_element_by_css_selector("#product-form > div > div.right.col-lg-7 > div.description > p").text.encode("utf-8")
		except:
			db.desc = ""
			
		db.stock = ""
		db.sale = ""#self.driver.find_element_by_css_selector("#right > div.detail > div:nth-child(2) > div > table > tbody > tr:nth-child(1) > td:nth-child(3)").text.encode("utf-8")
		db.set = ""
		db.custom = ""
		try:
			db.size = db.desc.split()[-1:][0]
		except:
			db.size = ""

		db.seller = ""

		try:
			db.min1 = self.driver.find_element_by_css_selector("#product-form > div > div.right.col-lg-7 > div.row.info > div:nth-child(5) > table > tbody > tr:nth-child(1) > td:nth-child(2)").text.encode("utf-8")
		except:
			db.min1 = 1

		db.price1 = self.driver.find_element_by_css_selector("#product-form > div > div.right.col-lg-7 > div.row.info > div:nth-child(6) > table > tbody > tr:nth-child(1) > td:nth-child(2) > span").text.encode("utf-8").split()[1]
		
		try:
			db.min2 = self.driver.find_element_by_css_selector("#product-form > div > div.right.col-lg-7 > div.row.info > div:nth-child(6) > table > tbody > tr:nth-child(2) > td:nth-child(3) > form > input.control").get_attribute("value")
		except:
			db.min2 = ""

		try:
			db.price2 = self.driver.find_element_by_css_selector("#product-form > div > div.right.col-lg-7 > div.row.info > div:nth-child(6) > table > tbody > tr:nth-child(2) > td:nth-child(2)").text.split()[1]
		except:
			db.price2 = ""

		db.mu2lti = db.min1
		db.d3ir400 = "kraftklub400"
		db.dir160 = "kraftklub160"
		db.img400 = self.driver.find_element_by_css_selector("#product-form > div > div.left.col-lg-5 > div > div:nth-child(1) > div > div > img").get_attribute("src")
		db.img160 = db.img400.split("/")[-1:][0]
		db.desc2 = ""
		db.option = ""
		db.dir800 = "kraftklub800"
		db.img800 = db.img160
		print db
		return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("term").clear()
                self.driver.find_element_by_name("term").send_keys(str(row))
                self.driver.find_element_by_name("term").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                continue

        try:
			self.links = []
			item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#home-right-bar-container > div > div > section > div.col-md-3.col-12 > div > div > div.product-name.col-12.no-padding > a") if a.get_attribute("href") not in self.links]
			print item
			self.links.extend(item)
			while self.nextPage():
				item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#home-right-bar-container > div > div > section > div.col-md-3.col-12 > div > div > div.product-name.col-12.no-padding > a") if a.get_attribute("href") not in self.links]
				print item
				self.links.extend(item)

			return self.links

        except:
            return None
