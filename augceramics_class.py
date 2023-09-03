from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class augceramics(domainobject.domainobject):

    vendor = "August Ceramics"
    url = "https://www.augustceramicswholesale.com/my-account/"
    home = "https://www.augustceramicswholesale.com/homepage/"
    uname = "tammy"
    passw = "Jones77x"
    delay = 1
    items = []
    
        
    def nextPage(self):
        try:
            self.driver.find_element_by_css_selector(".next").click()
            self.time.sleep(1)
            return True
        except:
            return False

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("username").send_keys(un)
        self.driver.find_element_by_name("password").send_keys(pw)
        self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector(".product_title").text.encode("utf-8")
        db.sku = db.name.split()[0]
        db.cat = "|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector(".woocommerce-breadcrumb > a")])
        try:
            db.desc = self.driver.find_element_by_css_selector("#tab-description").text.encode("utf-8")
        except:
            db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = self.driver.find_element_by_css_selector(".input-text").get_attribute("min")
        db.price1 = self.driver.find_element_by_css_selector(".price > span:nth-child(1)").text.encode("utf-8").replace("$","")
        try:
            db.min2 = self.driver.find_element_by_css_selector(".rp_wcdpd_pricing_table > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > span:nth-child(1)").text.split("+")[0]
            db.price2 = self.driver.find_element_by_css_selector(".rp_wcdpd_pricing_table > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > span:nth-child(1) > span:nth-child(1)").text.encode("utf-8").replace("$","")
        except:
            db.min2=""
            db.price2=""

        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "AugCeramics"
        db.dir160 = "AugCeramics"
		
        try:
            db.img400 = self.driver.find_element_by_css_selector(".woocommerce-product-gallery__image > a:nth-child(1)").get_attribute("href")
        except:
            return
			
        db.img160 = db.img400.split("/")[-1:][0]    
        db.desc2 = ""
        db.option = ""
        db.dir800 = "AugCeramics"
        db.img800 = db.img160     
        print db
        return db
        
        
    def search_item(self,row):
        # self.driver.find_element_by_css_selector("body > header > div.upper-header > button.upper-header-item.search-wrapper").click()
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("s").clear()
                self.driver.find_element_by_name("s").send_keys(str(row))
                self.driver.find_element_by_name("s").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        try:
            item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#content > ul > li > a.woocommerce-LoopProduct-link.woocommerce-loop-product__link")]
            print item
            self.items.extend(item)
            while self.nextPage():
                item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#content > ul > li > a.woocommerce-LoopProduct-link.woocommerce-loop-product__link")]
                print item
                self.items.extend(item)
            return self.items
        except:
            return None

