from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class mullberry(domainobject.domainobject):

    vendor = "Mullberry Home Wholesale"
    url = "https://www.mullberryhome.com/"
    home = "https://www.mullberryhome.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("email").send_keys(un)
        # self.driver.find_element_by_name("password").send_keys(pw)
        # self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("body > div.page-wrapper > div.breadcrumbs > ul > li.item.product > strong").text.encode("utf-8")
        try:
			db.sku = self.driver.find_element_by_css_selector("div[itemprop='item_number']").text.encode("utf-8")
        except:
			db.sku = ""
        db.cat = ""
        db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        try:
			db.size = self.driver.find_element_by_css_selector("div[itemprop='measurements']").text.encode("utf-8")
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
        db.dir400 = "Mulberry400"
        db.dir160 = "Mulberry160"
        # db.img400 = self.driver.find_element_by_css_selector("#MainForm > table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(1) > td:nth-child(1) > a > img").get_attribute("src")
        while True:
			try:
				db.img400 = self.driver.find_element_by_css_selector("img.fotorama__img").get_attribute("src")
				break
			except:
				self.time.sleep(1)
				continue
        if "nophoto" in db.img400:
            print "No photo detected..."
            return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = self.driver.find_element_by_css_selector("div[itemprop='sku']").text.encode("utf-8")
        db.option = ""
        db.dir800 = "Mulberry800"
        db.img800 = db.img160     
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
				self.driver.find_element_by_name("q").clear()
				self.driver.find_element_by_name("q").send_keys(str(row))
				self.driver.find_element_by_name("q").send_keys(self.Keys.ENTER)
				self.time.sleep(1)
				break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        try:
            item = self.driver.find_element_by_css_selector("#layer-product-list > div > div.products.wrapper.grid.products-grid > ol > li > div > div.product.details.product-item-details > div > strong > a").get_attribute("href")
            return [item]
        except:
            return

