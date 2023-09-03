from selenium.webdriver.common.keys import Keys
from table_gateway import gateway
import domainobject

class wingtai(domainobject.domainobject):

    vendor = "Wing Tai Trading"
    url = "http://www.wtcollectionshowroom.com/store/viewproducts.html"
    home = "https://wingtai.solovue.com/"
    uname = "service@waresitat.com"
    passw = "wolfville"
    login = "http://www.wtcollectionshowroom.com/cgi-wtcollectionshowroom/sb/order.cgi?func=2&storeid=*1209f4a48ae200708d5090&html_reg=html"
    delay = 1
    links = []
    
        
    def nextPage(self):
        print "Pagination attempt..."
        try:
            self.driver.find_elements_by_css_selector("input[value=Next]")[-1].click()
            self.time.sleep(1)
            return True
        except:
            print "Page exhausted.."
            return False

    def get_cats(self):
        ln = [l.get_attribute("href") for l in self.links.extself.driver.find_elements_by_css_selector("#loopproducts > div > div.loopprod.center > div.prodbasics > a") if l.get_attribute("href") not in self.links]
        ln = [l.get_attribute("href") for l in self.links.extself.driver.find_elements_by_css_selector("#ShopSite > li:nth-child(2) > div > ul > li:nth-child(1) > a") if l.get_attribute("href") not in self.links]
        print l
        return l

    def get_all_items(self):
        print "Getting all items..."
        self.driver.get(self.home)
        self.time.sleep(1)
        cats = self.get_cats()
        for cat in cats:
            self.driver.get(cat)
            self.time.sleep(1)
            self.get_info()
            while self.nextPage():
                self.get_info()


    def init_login(self,un,pw):
        self.driver.get(self.home)
        self.time.sleep(2)
        self.driver.find_element_by_css_selector("#pre-login-navbar > li.signIn-li > a").click()
        self.time.sleep(1)
        # self.driver.find_element_by_css_selector("#regPullLogin").click()
        # self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_id("username").send_keys(un)
        self.driver.find_element_by_id("password").send_keys(pw)
        self.driver.find_element_by_id("password").send_keys(Keys.ENTER)
        # self.driver.find_element_by_css_selector("#Sign\20 In").click()
        self.time.sleep(3)
        print "Success."

    def get_info_orig(self,sku=None):
        page_items = []
        print "Initiate grabbing items..."
        page_items.extend(self.save_info())
        while self.nextPage():
            page_items.extend(self.save_info())
        for page in page_items:
            print type(page)
        
        self.time.sleep(2)
        return page_items

    def get_info(self,sku=None):
        
        # print "Status: Looping each items"
        # dbs = []
        
        # items = self.driver.find_elements_by_css_selector("div[id^='loop'] > div")
        
        # for item in items:
            
        db = gateway()
        try:
            db.name = self.driver.find_element_by_css_selector("#moredesc").text.encode("utf-8")
            print db.name
        except:
            print "Skipping. Possible noise."
            # print self.driver.get_attribute("innerHTML")
            # continue #its possible that you'll get error from noise. Just skip and move to next div
        
        try:
            db.sku = self.driver.find_element_by_css_selector("#moreside > h1").text.encode("utf-8")
        except:
            # print self.driver.get_attribute("innerHTML")
            print "Skipping. Possible noise."
            # continue #possible noise
        
        db.cat = "" 
        db.desc = ""

        try:
            db.stock = self.driver.find_element_by_css_selector("div > span").text.encode("utf-8")
        except:
            db.stock = ""

        try:
            db.sale = self.driver.find_element_by_css_selector("#bb-mioptt").text.encode("utf-8")
        except:
            db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""

        try:
            db.min1 = self.driver.find_element_by_css_selector("td.qp_quantity:nth-child(2)").text.encode("utf-8")
            if "-" in db.min1:
                db.min1 = db.min1.split("-")[0].strip()
            db.price1 = self.driver.find_element_by_css_selector("td.qp_price:nth-child(2)").text.encode("utf-8").strip("$")

        except:
            db.min1 = ""
            db.price1 = ""

        try:
            db.min2 = self.driver.find_element_by_css_selector("td.qp_quantity:nth-child(3)").text.encode("utf-8")
            if "+" in db.min2:
                db.min2 = db.min2.strip("+").strip()
            if "-" in db.min2:
                db.min2 = db.min2.split("-")[0].strip()
            db.price2 = self.driver.find_element_by_css_selector("td.qp_price:nth-child(3)").text.encode("utf-8").strip("$")

        except:
            db.min2 = ""
            db.price2 = ""

        try:
            db.min3 = self.driver.find_element_by_css_selector("td.qp_quantity:nth-child(4)").text.encode("utf-8").strip("+")
            if "-" in db.min3:
                db.min3 = db.min3.split("-")[0].strip().strip("+")
            if "+" in db.min3:
                db.min3 = db.min3.strip().strip("+")
            db.price3 = self.driver.find_element_by_css_selector("td.qp_price:nth-child(4)").text.encode("utf-8").strip("$")

        except:
            db.min3 = ""
            db.price3 = ""

        db.multi = db.min1
        db.dir400 = "WingTai400"
        db.dir160 = "WingTai160"

        try:
            # db.img400 = self.driver.find_element_by_css_selector("#moreimage > div > img").get_attribute("src")
            db.img400 = self.driver.find_element_by_css_selector("#bb-miimghalf > div > img").get_attribute("src")

        except:
            print "Image not found. Placing dummy image url."
            db.img400 = "http://www.wtcollectionshowroom.com/store/media/noimage.jpg"

        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "WingTai800"
        db.img800 = db.img160
        print db.retrieve()
        # dbs.append(db)

        return db
        
        
    def search_item(self,row):
        
        while True:
			try:
				print "\nSearching for item: " + row+"\n"
				self.driver.find_element_by_name("search_field").clear()
				self.driver.find_element_by_name("search_field").send_keys(str(row))
				self.driver.find_element_by_name("search_field").send_keys(self.Keys.ENTER)
				self.time.sleep(2)
				break
			except:
				self.driver.get(self.home)
				self.time.sleep(1)
				continue
        try:
            item = self.driver.find_element_by_css_selector("#bb-loopproducts > li > div.item")
            return None
        except:
            return (["https://www.wtcollectionshowroom.com/store/"+row+"_moreinfo.html"])