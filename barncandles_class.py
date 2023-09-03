from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class barncandles(domainobject.domainobject):

    vendor = "Barn Candles"
    url = "https://www.barncandles.com/"
    sitemap = "https://www.barncandles.com/home-page-category-list.aspx"
    uname = "rick@waresitat.com"
    passw = "Wolfv!lle11"
    delay = 1
    links = []
    
        
    def get_all_items(self):
        self.driver.get(self.sitemap)
        self.time.sleep(1)

        item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#MainForm > div.Layout > section > div > div > section > div.LayoutContentInner > div.product-list > div > div > div > div > div.no-m-b > a") if a.get_attribute("href") not in self.links]
        print item
        self.links.extend(item)
        while self.nextPage():
            item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#MainForm > div.Layout > section > div > div > section > div.LayoutContentInner > div.product-list > div > div > div > div > div.no-m-b > a") if a.get_attribute("href") not in self.links]
            print item
            self.links.extend(item)

    def nextPage(self):
        try:
            a = [a for a in self.driver.find_elements_by_css_selector("#MainForm > div.Layout > section > div > div > section > div.LayoutContentInner > div:nth-child(14) > div > ul > li > a") if "Next" in a.text][0]
            a.click()
            self.time.sleep(1)
            return True
        except:
            print "Page Exhausted."
            return False

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element_by_css_selector("div > div.navbar-collapse.collapse > div > ul > li:nth-child(3) > a").click()
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("acctl3755$txtEmailAddress").send_keys(un)
        self.driver.find_element_by_name("acctl3755$txtPassword").send_keys(pw)
        self.driver.find_element_by_name("acctl3755$txtPassword").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        try:
			db.name = self.driver.find_element_by_css_selector("#MainForm > div.Layout > section > div > div > section > div.LayoutContentInner > div:nth-child(7) > div.clearfix > div:nth-child(1) > div > div:nth-child(2) > div.page-header.no-m-t > div > h1 > span").text.encode("utf-8")
			print name
        except:
			print "No name"

        try:
            db.sku = self.driver.find_element_by_css_selector("#lblItemNr").text.encode("utf-8")
        except:
            return

        db.cat = "|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("#lblCategoryTrail > a")])
        db.desc = self.driver.find_element_by_css_selector("#MainForm > div.Layout > section > div > div > section > div.LayoutContentInner > div:nth-child(7) > div.tab-content").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = self.driver.find_element_by_css_selector("#txtQuantity").get_attribute("value")
        db.price1 = self.driver.find_element_by_css_selector("#lblPrice").text.encode("utf-8")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "Barn400"
        db.dir160 = "Barn160"
        db.img400 = self.driver.find_element_by_css_selector("#MainForm > div.Layout > section > div > div > section > div.LayoutContentInner > div:nth-child(7) > div.clearfix > div:nth-child(1) > div > div.col-sm-6.thumbnail.no-overflow > a").get_attribute("href")
        if "nophoto" in db.img400:
            print "No photo detected..."
            return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Barn800"
        db.img800 = db.img160     
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_css_selector("div > div.navbar-collapse.collapse > div > ul > li:nth-child(1) > a").click()
                self.driver.find_element_by_name("txtRedirectSearchBox").clear()
                self.driver.find_element_by_name("txtRedirectSearchBox").send_keys(str(row))
                self.driver.find_element_by_name("txtRedirectSearchBox").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.get(self.url)
                self.time.sleep(1)
                continue

        item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#MainForm > div.Layout > section > div > div > section > div.LayoutContentInner > div.product-list > div > div > div > div > div.no-m-b > a") if a.get_attribute("href") not in self.links]
        print item
        self.links.extend(item)
        while self.nextPage():
            item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#MainForm > div.Layout > section > div > div > section > div.LayoutContentInner > div.product-list > div > div > div > div > div.no-m-b > a") if a.get_attribute("href") not in self.links]
            print item
            self.links.extend(item)

