from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class birchmaison(domainobject.domainobject):

    vendor = "Craft Outlet - Olde Memories"
    url = "https://birchmaison.com/"
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
        try:
            db.name = self.driver.find_element_by_css_selector(".product_name").text.encode("utf-8")
        except:
            self.driver.refresh()
            self.time.sleep(1)
            db.name = self.driver.find_element_by_css_selector(".product_name").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector(".sku > span:nth-child(1)").text.encode("utf-8")
        db.cat = "|".join([c.text.encode("utf-8") for c in self.driver.find_elements_by_css_selector(".breadcrumb_text > span")])
        try:
            db.desc = self.driver.find_element_by_css_selector(".description > p:nth-child(1)").text.encode("utf-8")
        except:
            try:
                db.desc = self.driver.find_element_by_css_selector("#shopify-section-product-template > div.container.main.content > div.product.clearfix > div > div > div.section.product_section.clearfix.js-product_section > div.seven.columns.omega > div.description").text.encode("utf-8")
            except:
                db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        try:
            db.size = self.driver.find_element_by_css_selector(".single-option-selector option").get_attribute("value")
        except:
            db.size = ""
        db.seller = ""
        db.min1 = ""
        db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "CraftOutlet400"
        db.dir160 = "CraftOutlet160"
        try:
            db.img400 = self.driver.find_element_by_css_selector("#shopify-section-product-template > div.container.main.content > div.product.clearfix > div > div > div.section.product_section.clearfix.js-product_section > div.nine.columns.alpha > div > div > div > div > div > a > div > img").get_attribute("src")
        except:
            db.img400 = ""
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "CraftOutlet800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
		print "\nSearching for item: " + row+"\n"
		while True:
			try:
				self.driver.find_element_by_css_selector("#shopify-section-header > header:nth-child(2) > div > div.main_nav_wrapper > div > div.nav > ul > li.search_container > form > input[type=text]:nth-child(3)").clear()
				self.driver.find_element_by_css_selector("#shopify-section-header > header:nth-child(2) > div > div.main_nav_wrapper > div > div.nav > ul > li.search_container > form > input[type=text]:nth-child(3)").send_keys(row)
				self.driver.find_element_by_css_selector("#shopify-section-header > header:nth-child(2) > div > div.main_nav_wrapper > div > div.nav > ul > li.search_container > form > input[type=text]:nth-child(3)").send_keys(self.Keys.ENTER)
				self.time.sleep(1)
				break
			except Exception as e:
				print "Search fail:"
				print e
				self.driver.refresh()
				self.time.sleep(1)
				continue
		try:
			item = self.driver.find_element_by_css_selector(".product-info__caption").get_attribute("href")
			print item
			return [item]
		except:
			return None

