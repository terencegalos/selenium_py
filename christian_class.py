from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class christian(domainobject.domainobject):

    vendor = "Christian Art Gifts"
    url = "https://www.christianartgifts.com/"
    home = "https://www.christianartgifts.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("login[username]").send_keys(un)
        # self.driver.find_element_by_name("login[password]").send_keys(pw)
        # self.driver.find_element_by_name("login[password]").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element_by_css_selector("#item-detail-wrap > div.view-body.item-detail-page > div.row-fluid > div.span6.item-detail-info-wrap > div > h1").text.encode("utf-8")
        except:
            return
        db.sku = self.driver.find_element_by_css_selector("#item-detail-wrap > div.view-body.item-detail-page > div.row-fluid > div.span6.item-detail-info-wrap > div > div.item-detail-information.row-fluid > div.span3 > span:nth-child(2)").text.encode("utf-8")
        db.cat = "|".join([a.text for a in self.driver.find_elements_by_css_selector("#item-detail-wrap > div.view-header > div > div > ul > li > a")])
        db.desc = self.driver.find_element_by_css_selector("#collapsed-0 > div").text.encode("utf-8")
        # db.stock = self.driver.find_element_by_css_selector("#commerce > div > table > tbody > tr > td:nth-child(2) > table:nth-child(1) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(3) > td:nth-child(2)").text.encode("utf-8")
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
        db.dir400 = "ChristianArt400"
        db.dir160 = "ChristianArt160"
        # self.time.sleep(1)
        try:
            db.img400 = self.driver.find_element_by_css_selector("#item-detail-wrap > div.view-body.item-detail-page > div.row-fluid > div.span6.item-detail-image-wrap > div.item-image-gallery > div > div.bx-viewport > ul > li:nth-child(2) > img").get_attribute("src").split("?")[0]
        except:
            db.img400 = self.driver.find_element_by_css_selector("#item-detail-wrap > div.view-body.item-detail-page > div.row-fluid > div.span6.item-detail-image-wrap > div.item-image-gallery > div > img").get_attribute("src").split("?")[0]
        # db.img400 = self.driver.find_element_by_css_selector("#item-detail-wrap > div.view-body.item-detail-page > div.row-fluid > div.span6.item-detail-image-wrap > div.item-image-gallery > div > div.bx-viewport > ul > li:nth-child(2) > img").get_attribute("src").split("?")[0]
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "ChristianArt800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
		print "\nSearching for item: " + row+"\n"
		while True:
			try:
				self.driver.find_element_by_css_selector("#site-search-container-fake > form > div").click()
				self.time.sleep(1)
				
				self.driver.find_element_by_css_selector("#masive-search > form > div > input").clear()
				self.driver.find_element_by_css_selector("#masive-search > form > div > input").send_keys(str(row))
				self.time.sleep(1)
				self.driver.find_element_by_css_selector("#masive-search > form > div > input").send_keys(Keys.ENTER)
				self.time.sleep(1)
				break
			except:
				self.driver.refresh()
				self.time.sleep(1)
				continue
		
		items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#item-list > div.infinite-divider > div > div > div > div > div.cag-item-cell-content > div.cag-item-cell-title > a")]
		return items
