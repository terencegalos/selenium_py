from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class thecountryhouse(domainobject.domainobject):

    vendor = "The Country House Collection"
    url = "https://www.thecountryhouse.com"
    sitemap = "https://www.thecountryhouse.com/site_map.asp"
    uname = "waresitat"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("username").send_keys(un)
        # self.driver.find_element_by_name("passwd").send_keys(pw)
        # self.driver.find_element_by_name("passwd").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector(".productName").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#content div.productPage div.productDetails p:nth-child(1)").text.encode("utf-8").split(":")[1]
        db.cat = ""
        try:
			db.desc = self.driver.find_element_by_css_selector("#content > div.productPage > div.productDetails > p:nth-child(3)").text.encode("utf-8")
        except:
			db.desc = ""
        db.stock = ""
        try:
            db.sale = self.driver.find_element_by_css_selector("span.specialprice").text.encode("utf-8")
        except:
            db.sale = ""
        db.set = ""
        db.custom = ""
        try:
			db.size = self.driver.find_element_by_css_selector("#content > div.productPage > div.productDetails > p:nth-child(4)").text.encode("utf-8")
        except:
			db.size = ""
        db.seller = ""
        try:
            db.min1 = self.driver.find_element_by_css_selector("#vmMainPage div.Product-border div div:nth-child(1) div.floatElement div.product-divider div.browsePriceContainer table tbody tr:nth-child(1) td:nth-child(1)").text.encode("utf-8")
        except:
			try:
				db.min1 = self.driver.find_element_by_css_selector("#content > div.productPage > div.productDetails > form > input.qtyBox").get_attribute("value")
			except:
				db.min1 = ""
        db.price1 = self.driver.find_element_by_css_selector("p.productPrice").text.encode("utf-8")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "TheCountryHouse400"
        db.dir160 = "TheCountryHouse160"
        db.img400 = self.driver.find_element_by_css_selector("#content div.productPage div.productImg img").get_attribute("src").split("?")[0]
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "TheCountryHouse800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("Description").click()
                self.time.sleep(1)
                self.driver.find_element_by_name("Description").clear()
                self.driver.find_element_by_name("Description").send_keys(str(row))
                self.driver.find_element_by_name("Description").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                continue

        return None

# ongoing dev
def get_cat(self):
    all = ["http://www.thecountryhouse.com/viewcategory.asp?catid=126","http://www.thecountryhouse.com/viewcategory.asp?catid=125","http://www.thecountryhouse.com/viewcategory.asp?catid=93","http://www.thecountryhouse.com/viewcategory.asp?catid=100","http://www.thecountryhouse.com/viewcategory.asp?catid=112","http://www.thecountryhouse.com/viewcategory.asp?catid=153"]
    cats = br.find_elements_by_css_selector("#content > table > tbody > tr:nth-child(1) > td:nth-child(2) > strong:nth-child(2) > a")
    cats = br.find_elements_by_css_selector("#content > table > tbody > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(24) > a")
    cats = br.find_elements_by_css_selector("#content > table > tbody > tr:nth-child(1) > td:nth-child(3) > strong:nth-child(30) > a")
    cats = br.find_elements_by_css_selector("#content > table > tbody > tr:nth-child(1) > td:nth-child(3) > strong:nth-child(32) > a")
    
