from helper.table_gateway import gateway
import helper.domainobject
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json

class chc(domainobject.domainobject):

    vendor = "Country Home Creations"
    url = "https://countryhomecreations.com/"
    home = "https://countryhomecreations.com/"
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
        # print "Logging in..."
        # self.driver.find_element_by_name('customer[email]').send_keys(un)
        # self.driver.find_element_by_name('customer[password]').send_keys(pw)
        # self.driver.find_element_by_name('customer[password]').send_keys(Keys.ENTER)
        # driver.find_element_by_css_selector("#customer_login > div.row > div.col-sm-5.col-ms-6.col-xs-4 > p > input").click()
        print "Login Success."
        self.time.sleep(1)
        # except:
            # print "Login failed."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#shopify-section-product > div:nth-child(1) > div > div > div.grid__item.medium-up--one-half.product__form__wrapper > div:nth-child(1) > div.product__title__wrapper > h1").text.encode("utf-8")
        print self.driver.find_element_by_css_selector("#shopify-section-product > div:nth-child(1) > script").text
        db.sku = item#json.loads(self.driver.find_element_by_css_selector("#shopify-section-product > div:nth-child(1) > script").text)["sku"]
        # except:
			# db.sku = item
        db.cat = ""
        try:
            db.desc =  self.driver.find_element_by_css_selector("#shopify-section-product-template > div:nth-child(2) > div > div > div.seven.columns.omega > div.description").text.encode("utf-8")
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
        db.dir400 = "CountryHome400"
        db.dir160 = "CountryHome160"
        db.img400 = "https"+self.driver.find_element_by_css_selector("#slick-slide00 > div > div > img").get_attribute("data-srcset")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "CountryHome800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
		print "\nSearching for item: " + row+"\n"
		self.driver.find_element_by_css_selector("#shopify-section-header > div > div > div.header--desktop.small--hide > nav > div.nav__search > a").click()
		self.time.sleep(1)
		self.driver.find_element_by_css_selector("#HeaderSearch").clear()
		self.driver.find_element_by_css_selector("#HeaderSearch").send_keys(str(row))
		self.driver.find_element_by_css_selector("#HeaderSearch").send_keys(self.Keys.ENTER)
		self.time.sleep(1)
		
		
		try:
			item = self.driver.find_element_by_css_selector("#MainContent > div > div > div > div.grid__item.five-sixths > p.h3--body > a").get_attribute("href")
			print item
			return [item]
		except:
			return None

