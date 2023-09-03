from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class olivia(domainobject.domainobject):

    vendor = "Market Street Wholesale"
    url = "http://www.marketstreetwholesale.com/"
    home = "http://www.marketstreetwholesale.com/"
    uname = "kaye.williams@waresitat.com"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # self.driver.find_element_by_css_selector("#external_links > ul.hidden-xs.nav.navbar-nav.navbar-right > li:nth-child(2) > a > span > i").click()
        # self.time.sleep(1)
        # self.driver.find_element_by_css_selector("#external_links > ul.hidden-xs.nav.navbar-nav.navbar-right > li.dropdown-grid.no-open-arrow.open > div > div > div > div.login_frm > div > a:nth-child(1)").click()
        # self.time.sleep(1)
        
        # try:
        #     print "Logging in..."
        #     self.driver.find_element_by_name('customer[email]').send_keys(un)
        #     self.driver.find_element_by_name('customer[password]').send_keys(pw)
        #     self.driver.find_element_by_name('customer[password]').send_keys(Keys.ENTER)
        #     driver.find_element_by_css_selector("#customer_login > div.row > div.col-sm-5.col-ms-6.col-xs-4 > p > input").click()
        #     print "Login Success."
        #     self.time.sleep(2)
        # except:
        #     print "Login failed."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#main-content > div.container > div > div.productView > section.productView-details.product-data > div > h1").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#main-content > div.container > div > div.productView > section.productView-details.product-data > div > dl > dd:nth-child(2)").text.encode("utf-8")
        # except:
			# db.sku = item
        try:
            db.cat = "|".join([c.text for c in self.driver.find_elements_by_css_selector("body > div.body > div.container > ul > li.breadcrumb")])
        except:
            db.cat = ""
        try:
            db.desc =  self.driver.find_element_by_css_selector("#tab-description").text.encode("utf-8")
        except:
            db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
			db.min1 = self.driver.find_element_by_css_selector("body > div.body > div.container > div > div.productView > section:nth-child(1) > div > dl > dd:nth-child(4)").text.encode("utf-8")
        except:
			try:
				db.min1 = self.driver.find_element_by_name("qty[]").get_attribute("value")
			except:
				db.min1 = 1
        db.price1 = 99
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "olivias400"
        db.dir160 = "olivias160"
        try:
            db.img400 = self.driver.find_element_by_css_selector("#main-content > div.container > div > div.productView > section.productView-images > figure > div > a").get_attribute("href").split("?")[0]
        except:
            print "Image not detected."
            return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "olivias800"
        db.img800 = db.img160
        try:
			print db
        except:
			print "Item not complete."
        return db
        
        
    def search_item(self,row):
		print "\nSearching for item: " + row+"\n"
		while True:
			try:
				try:
					self.driver.find_element_by_css_selector("#quick-search-expand").click()
				except:
					self.driver.find_element_by_css_selector("body > header > nav > ul > li a']").click()
				self.time.sleep(1)
				self.driver.find_element_by_name("nav-quick-search").clear()
				self.driver.find_element_by_name("nav-quick-search").send_keys(str(row))
				self.driver.find_element_by_name("nav-quick-search").send_keys(self.Keys.ENTER)
				self.time.sleep(1)
				break
			except:
				self.driver.get(self.url)
				self.time.sleep(1)
				continue

		try:
			item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("div.listItem-details > h4 > a")][0]
			return [item]
		except:
			return  None

