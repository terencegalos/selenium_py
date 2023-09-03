from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class jjwire(domainobject.domainobject):

    vendor = "J&J Wire"
    url = "https://jjwire.biz/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
		self.driver.get(self.url)
		self.time.sleep(1)
        # try:
            # self.driver.find_element_by_css_selector("#JS_PROD > div.content-container > div > div > div > div.row > div.col-sm-7 > div.well.well-prod > a").click()
        # except:
            # self.driver.get(self.url)
        # self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("Customer_LoginEmail").send_keys(un)
        # self.driver.find_element_by_name("Customer_Password").send_keys(pw)
        # self.driver.find_element_by_name("Customer_Password").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
		db = gateway()
		db.name = self.driver.find_element_by_css_selector("div.summary.entry-summary > h1").text.encode("utf-8")
		try:
			db.sku = self.driver.find_element_by_css_selector("div.summary.entry-summary > div.product_meta > span.sku_wrapper > span").text.encode("utf-8")
		except:
			db.sku = item
		db.cat = self.driver.find_element_by_css_selector("div.summary.entry-summary > div.product_meta > span.posted_in > a").text.encode("utf-8")
		try:
			db.desc = self.driver.find_element_by_css_selector("#tab-description > p").text.encode("utf-8")
		except:
			db.desc = ""
		db.stock = ""
		db.sale = ""
		db.set = ""
		db.custom = ""
		db.size = ""
		db.seller = ""
		db.min1 = ""
		db.price1 = ""
		db.min2 = ""
		db.price2 = ""
		db.min3 = ""
		db.price3 = ""
		db.multi = ""
		db.dir400 = "jjwire400"
		db.dir160 = "jjwire160"
		try:
			db.img400 = self.driver.find_element_by_css_selector("div.images > a").get_attribute("href")
		except:
			db.img400 = ""
		db.img160 = db.img400.split("/")[-1:][0]
		db.desc2 = ""
		db.option = ""
		db.dir800 = "jjwire800"
		db.img800 = db.img160
		print db
		return db
        
        
    def search_item(self,row):
		print "\nSearching for item: " + row+"\n"
		while True:
			try:
				self.driver.find_element_by_css_selector("input.search-field").clear()
				self.driver.find_element_by_css_selector("input.search-field").send_keys(row)
				self.driver.find_element_by_css_selector("input.search-field").send_keys(self.Keys.ENTER)
				self.time.sleep(1)
				break
			except Exception as e:
				print "Search fail:"
				print e
				self.driver.get(url)
				self.time.sleep(1)
				continue
		try:
			item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("body > div.pagecontents > div > div > ul.products > li > a.woocommerce-LoopProduct-link.woocommerce-loop-product__link")]
			# item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("body > div.pagecontents > div > div.grid_9 > ul > li.first.post-4625.product.type-product.status-publish.has-post-thumbnail.product_cat-candle-accessories.instock.shipping-taxable.purchasable.product-type-simple > a")]
			print item
			return item
		except:
			return None

