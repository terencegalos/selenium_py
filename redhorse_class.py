from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class redhorse(domainobject.domainobject):

    vendor = "Red Horse Signs"
    url = "https://www.redhorsesigns.com/"
    home = "https://www.redhorsesigns.com/"
    uname = "service@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("q").send_keys(un)
        # self.driver.find_element_by_name("q").send_keys(pw)
        # self.driver.find_element_by_name("q").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("div.product-name > h1").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("div.product-name > p > strong").text.encode("utf-8")
        db.cat = ""
        db.desc = self.driver.find_element_by_css_selector("div.short-description > div").text.encode("utf-8")
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
        db.dir400 = "RedHorse400"
        db.dir160 = "RedHorse160"
        # db.img400 = self.driver.find_element_by_css_selector("#MainForm > table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(1) > td:nth-child(1) > a > img").get_attribute("src")
        db.img400 = self.driver.find_element_by_css_selector("img.zoomImg").get_attribute("src")
        if "nophoto" in db.img400:
            print "No photo detected..."
            return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "RedHorse800"
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
				self.driver.refresh()
				self.time.sleep(1)
				continue
		try:
			item = self.driver.find_element_by_css_selector("h2.product-name a").get_attribute("href")
			return [item]
		except:
			return None