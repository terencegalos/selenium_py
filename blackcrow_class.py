from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class blackcrow(domainobject.domainobject):

    vendor = "Black Crow Candles"
    url = "https://blackcrowcandlecompany.com/account/login"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    links = []
        
    def nextPage(self):
        print "Page exhausted"
        return False

    def get_items(self):
        ln = [l.get_attribute("href") for l in self.driver.find_elements_by_css_selector("main > div > div.grid__item.large--four-fifths > div > div > a") if l.get_attribute("href") not in self.links]
        print ln
        return ln

    def get_all_links(self):
        # cats = [cat.get_attribute("href") for cat in self.driver.find_elements_by_css_selector("#AccessibleNav > li > a")]
        self.driver.get("https://blackcrowcandlecompany.com/collections/")
        self.time.sleep(1)
        cats = [cat.get_attribute("href") for cat in self.driver.find_elements_by_css_selector("#collections > main > div > div.grid__item.large--four-fifths > div > div > a")]
        for cat in cats:
            print "Get request: " + cat
            self.driver.get(cat)
            self.time.sleep(2)
            self.links.extend(self.get_items())
            while self.nextPage():
                self.links.extend(self.get_items())

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(5)
        
        print "Logging in."
        self.driver.find_element_by_css_selector("#CustomerEmail").send_keys(un)
        self.driver.find_element_by_css_selector("#CustomerPassword").send_keys(pw)
        self.driver.find_element_by_css_selector("#CustomerPassword").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def save_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("main > div > div.grid__item.large--four-fifths > div > div.product-single > div.grid.product-single__hero > div:nth-child(2) > h1").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("main > div > div.grid__item.large--four-fifths > div > div.product-single > div.grid.product-single__hero > div:nth-child(2) > h1").text.encode("utf-8")
        try:
            db.cat = self.driver.find_element_by_css_selector("main > div > div.grid__item.large--four-fifths > div > div.section-header.section-header--breadcrumb > nav > a:nth-child(3)").text.encode("utf-8")
        except:
            db.cat = ""
        db.desc = self.driver.find_element_by_css_selector("#tab-1").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = self.driver.find_element_by_css_selector("#Quantity").get_attribute("value")
        db.price1 = self.driver.find_element_by_css_selector("#ProductPrice").text.encode("utf-8")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = self.driver.find_element_by_css_selector("#Quantity").get_attribute("value")
        db.dir400 = "blackcrow400"
        db.dir160 = "blackcrow160"
        db.img400 = self.driver.find_element_by_css_selector("#ProductPhotoImg").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0].split("?")[0]
        db.desc2 = ""
        try:
            db.option = "|".join([opt.text for opt in self.driver.find_elements_by_css_selector("#productSelect-option-0 > option")])
        except:
            db.option = ""
        db.dir800 = "blackcrow800"
        db.img800 = db.img160
        print db
        return db

    def get_info(self,item=None):
        while True:
            try:
                db = self.save_info()
                return db
                break
            except:
                self.init_login(self.uname,self.passw)
                db = self.save_info()
                return db
                break
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        # if len(row.split(",")[1].strip()) > 1:
        while True:
            try:
                self.driver.find_element_by_name("Search").clear()
                self.driver.find_element_by_name("Search").send_keys(row)
                self.driver.find_element_by_name("Search").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except Exception as e:
                print "Search fail:"
                print e
                self.driver.refresh()
                self.time.sleep(1)
                continue
        try:
            items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#JS_SRCH > div.content-container > div > div > div > div.row.row-masonry > div.ctgy-item > a")]
            return items
        except:
            return None
            

