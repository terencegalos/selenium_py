from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class wildwings(domainobject.domainobject):

    vendor = "Wild Wings"
    home = "https://wildwings.com/"
    login = "https://wildwings.com/account/login"
    uname = "service@waresitat.com"
    passw = "wolfville"
    delay = 1
    links = []
    
        
    def nextPage(self):
        try:
            if len(self.driver.find_elements_by_css_selector("a.PageArrow")) == 2:
                self.driver.find_elements_by_css_selector("a.PageArrow")[0].click()
            else:
                self.driver.find_elements_by_css_selector("a.PageArrow")[1].click()

            self.time.sleep(1)
            return True
        except:
            print "Page exhausted."
            return False
        
    def get_links(self):
        items = [l.get_attribute("href") for l in self.driver.find_elements_by_css_selector("div.thumbnail-grid.clearfix > div > div > div.info > a")]
        print items
        return items

    def get_all_items(self):
        cats = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#ctl00_myheader_headerPostLogin > nav > div > ul > li > a")]
        for cat in cats:
            print cat
            self.driver.get(cat)
            self.time.sleep(1)

            self.links.extend(self.get_links())
            while self.nextPage():
                self.links.extend(self.get_links())

    def init_login(self,un,pw):
        self.driver.get(self.login)
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_id("customer_email").send_keys(un)
        self.driver.find_element_by_id("customer_password").send_keys(pw)
        self.driver.find_element_by_id("customer_password").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."
        inp = raw_input("Done?")
        while inp is "n":
            raw_input("Done?")

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("h1.m_ipad_hide").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector(".sku").text.encode("utf-8")
        db.cat = ""
        try:
            db.desc = self.driver.find_element_by_css_selector("#tab1 > p:nth-child(1)").text.encode("utf-8")
        except:
            self.driver.refresh()
            self.time.sleep(1)
            db.desc = self.driver.find_element_by_css_selector("#tab1").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = 1
        db.price1 = 99
        # try:
		# 	db.price1 = self.driver.find_element_by_css_selector("span.RegularPrice").text.encode("utf-8")
        # except:
		# 	db.price1 = self.driver.find_element_by_css_selector("span.variantprice").text.encode("utf-8")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "wildwings400"
        db.dir160 = "wildwings160"
        db.img400 = self.driver.find_element_by_css_selector(".zoomImg").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "wildwings800"
        db.img800 = db.img160     
        print db
        self.time.sleep(5)
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("q").clear()
                self.driver.find_element_by_name("q").send_keys(str(row))
                self.driver.find_element_by_name("q").send_keys(self.Keys.ENTER)
                self.time.sleep(2)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("div.one-third > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(2)")]
        return items

