from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class dns(domainobject.domainobject):

    vendor = "DNS Designs"
    url = "http://www.dnsdesignsandmore.com/index.php"
    home = "http://www.dnsdesignsandmore.com/index.php"
    login = "http://www.dnsdesignsandmore.com/index.php?route=account/login"
    sitemap = "https://www.dnsdesignsandmore.com/index.php?route=information/sitemap"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 2
    allitems = []
    lastPage = ""
    stopFlag = False
    
        
    def nextPage(self):
        try:
            btn = self.driver.find_element_by_link_text(">")
            btn.click()
            self.time.sleep(1)
            return True
        except:
            return False

    def get_cat_items(self):
        self.driver.get("https://www.dnsdesignsandmore.com/index.php?route=information/sitemap")
        self.time.sleep(1)
        # scat = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#content > div.sitemap-info > div.left > ul > li > a")]
        scat = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#content > div.sitemap-info > div.left  a")]
        for c in scat:
            # try:
            print "***********************"
            print c
            self.driver.get(c)
            self.time.sleep(1)

            item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("div.name a")]
            print item
            self.allitems.extend(item)

            while self.nextPage():
                item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("div.name a")]
                print list(item)
                self.allitems.extend(list(item))
                print item
        return self.allitems

    def init_login(self,un,pw):
        self.driver.get(self.login)
        
        print "Logging in."
        self.driver.find_element_by_name("email").send_keys(un)
        self.driver.find_element_by_name("password").send_keys(pw)
        self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
        print "Success."


    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#content > h1").text.encode("utf-8")
        try:
			db.sku = self.driver.find_element_by_css_selector("div.description").text.encode("utf-8").split()[2]
        except:
			return
        db.cat = "|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("div.breadcrumb a")])
        db.desc = ""
        db.stock = self.driver.find_element_by_css_selector("#content > div.product-info > div.right > div.description").text.split("\n")[1]
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = self.driver.find_element_by_css_selector("#content > div.product-info > div.right > div.cart > div:nth-child(1) > input[type=\"text\"]:nth-child(1)").get_attribute("value")
        db.price1 = (self.driver.find_element_by_css_selector("#content > div.product-info > div.right > div.price").text.split("\n")[0]).split(":")[1]
        db.price1 = (self.driver.find_element_by_css_selector("#content > div.product-info > div.right > div.price").text.split("\n")[0]).split(":")[1]
        try:
			db.min2 = self.driver.find_element_by_css_selector("#content > div.product-info > div.right > div.price > div").text.split("or more")[0]
			db.price2 = self.driver.find_element_by_css_selector("#content > div.product-info > div.right > div.price > div").text.split("or more")[1].split()[0]
        except:
			db.min2 = ""
			db.price2 = ""
            
        try:
            db.min3 = self.driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/div[2]/div').text.split()[-4]
            db.price3 = self.driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/div[2]/div').text.split()[-1]
        except:
            db.min3 = ""
            db.price3 = ""
        db.multi = db.min1
        db.dir400 = "DNS400"
        db.dir160 = "DNS160"
        try:
			# db.img400 = self.driver.find_element_by_css_selector("#wrap > section:nth-child(2) > div > div > div > div:nth-child(3) > a").get_attribute("href")
			db.img400 = self.driver.find_element_by_css_selector("div.image a").get_attribute("href")
        except Exception as e:
			print e
			self.time.sleep(3)
			return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = self.driver.current_url
        db.option = ""
        db.dir800 = "DNS800"
        db.img800 = db.img160
        print db
        self.time.sleep(1)
        # if ".jpg" not in  db.img160:
            # return
        return db
        
        
    def search_item(self,row):
        self.allitems = []
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
				self.driver.find_element_by_name("filter_name").clear()
				self.driver.find_element_by_name("filter_name").send_keys(str(row))
				self.driver.find_element_by_name("filter_name").send_keys(Keys.ENTER)
				self.time.sleep(self.delay)
				break
            except:
                self.driver.get(self.url)
                self.time.sleep(self.delay)
                continue

        item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#content > div.product-grid > div > div.image > a")]
        self.allitems.extend(item)
        while self.nextPage():
            item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#content > div.product-grid > div > div.image > a")]
            self.allitems.extend(item)
            print item
        
        return self.allitems


