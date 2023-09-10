from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class crosswalks(domainobject.domainobject):

    vendor = "Crosswalks"
    url = "https://www.thassociates.biz/brand/wild-cotton"
    login = "https://www.thassociates.biz/"
    home = "https://www.thassociates.biz/"
    lastStop = "https://kraftklub.com/kg1621-860-lw"
    flag = False
    uname = "manvindersingh80@gmail.com"
    passw = "manvindersingh80"
    delay = 1
    links = []
    
    def init_login(self,un,pw):
        self.driver.get(self.login)
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("tpusername").send_keys(un)
        self.driver.find_element_by_name("tppassword").send_keys(pw)
        # resp = True
        # while resp:
			
		# 	inp = raw_input("Ready?")
		# 	if inp.lower() == "yes":
		# 		resp = False

        self.driver.find_element_by_name("tppassword").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."
        
    def nextPage(self):
		try:
			self.driver.find_element_by_css_selector("a.page-link.Next.navigationPage").click()
			self.time.sleep(3)
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
		db.name = self.driver.find_element_by_css_selector("body > div > div.proDetails > div.card > div > div > form > div > h3").text.encode("utf-8")
		db.sku = self.driver.find_element_by_css_selector("body > div > div.proDetails > div.card > div > div > form > div > p:nth-child(3)").text.encode("utf-8")
		db.cat = ""#"|".join([c.text.encode("utf-8") for c in self.driver.find_elements_by_css_selector("#location > a")])

		try:
			db.desc = self.driver.find_element_by_css_selector("body > div > div.proDetails > div.card > div > div > form > div > div:nth-child(11) > p").text.encode("utf-8")
		except:
			db.desc = ""
			
		db.stock = ""
		db.sale = ""#self.driver.find_element_by_css_selector("#right > div.detail > div:nth-child(2) > div > table > tbody > tr:nth-child(1) > td:nth-child(3)").text.encode("utf-8")
		db.set = ""
		db.custom = ""
		try:
			db.size = ""#b.desc.split()[-1:][0]
		except:
			db.size = ""

		db.seller = ""

		try:
			db.min1 = self.driver.find_element_by_css_selector("body > div > div.proDetails > div.card > div > div > form > div > table > tbody > tr > td:nth-child(2)").text.encode("utf-8")
		except:
			db.min1 = 1

		db.price1 = self.driver.find_element_by_css_selector("body > div > div.proDetails > div.card > div > div > form > div > table > tbody > tr > td:nth-child(1)").text.encode("utf-8")
		
		try:
			db.min2 = self.driver.find_element_by_css_selector("body > div > div.proDetails > div.card > div > div > form > div > table > tbody > tr:nth-child(2) > td:nth-child(2)").text
		except:
			try:
				db.min2 = self.driver.find_element_by_css_selector("#product-form > div > div.right.col-lg-7 > div.row.info > div:nth-child(6) > table > tbody > tr:nth-child(2) > td:nth-child(3) > form > select > option:nth-child(1)").get_attribute("value")
			except:
				db.min2 = ""

		try:
			db.price2 = self.driver.find_element_by_css_selector("body > div > div.proDetails > div.card > div > div > form > div > table > tbody > tr:nth-child(2) > td:nth-child(1)").text
		except:
			db.price2 = ""
		try:
			db.min3 = self.driver.find_element_by_css_selector("body > div > div.proDetails > div.card > div > div > form > div > table > tbody > tr:nth-child(2) > td:nth-child(2)").text
		except:
			try:
				db.min3 = self.driver.find_element_by_css_selector("body > div > div.proDetails > div.card > div > div > form > div > table > tbody > tr:nth-child(3) > td:nth-child(2)").text
			except:
				db.min3 = ""
		try:
			db.price3 = self.driver.find_element_by_css_selector("body > div > div.proDetails > div.card > div > div > form > div > table > tbody > tr:nth-child(2) > td:nth-child(1)").text
		except:
			db.price3 = ""

		db.multi = db.min1
		db.dir400 = "kraftklub400"
		db.dir160 = "kraftklub160"
		db.img400 = self.driver.find_element_by_css_selector("#pic_1 > a").get_attribute("href")
		db.img160 = db.img400.split("/")[-1:][0]
		db.desc2 = ""
		db.option = ""
		db.dir800 = "kraftklub800"
		db.img800 = db.img160
		print db
		return db
        
        
    def search_item(self,row):
        
        if self.driver.current_url == self.url:
            print "Proceeding search..."
        else:
            self.driver.get(self.url)

        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("productName").clear()
                self.driver.find_element_by_name("productName").send_keys(str(row))
                self.driver.find_element_by_id("searchProduct").click()
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                continue

        # self.driver.find_element_by_css_selector("#showPageProd > b > label > select > option:nth-child(5)").click()
        # self.time.sleep(3)
        try:
			self.links = []
			item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#listedproduct > div > form > div > a") if a.get_attribute("href") not in self.links]
			print item
			self.links.extend(item)
			while self.nextPage():
				item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#listedproduct > div > form > div > a") if a.get_attribute("href") not in self.links]
				print item
				self.links.extend(item)

			return self.links

        except:
            return None
        