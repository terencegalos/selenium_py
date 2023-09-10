from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class pbk(domainobject.domainobject):

    vendor = "Primitives by Kathy 50% Off Closeouts"
    url = "https://www.primitivesbykathy.com/"
    home = "https://www.primitivesbykathy.com/"
    uname = "kaye.williams@waresitat.com"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # self.driver.find_element_by_css_selector("#external_links > ul.hidden-xs.nav.navbar-nav.navbar-right > li:nth-child(2) > a > span > i").click()
        # self.time.sleep(1)
        # self.driver.find_element_by_css_selector("#external_links > ul.hidden-xs.nav.navbar-nav.navbar-right > li.dropdown-grid.no-open-arrow.open > div > div > div > div.login_frm > div > a:nth-child(1)").click()
        # self.time.sleep(1)
        
        # try:
        # print "Logging in..."
        # self.driver.find_element_by_name('customer[email]').send_keys(un)
        # self.driver.find_element_by_name('customer[password]').send_keys(pw)
        # self.driver.find_element_by_name('customer[password]').send_keys(Keys.ENTER)
        # driver.find_element_by_css_selector("#customer_login > div.row > div.col-sm-5.col-ms-6.col-xs-4 > p > input").click()
        print "Login Success."
        self.time.sleep(1)
        # except:
            # print "Login failed."

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element_by_css_selector("#content > article > div.product__heading.md-6.md-right > h1").text.encode("utf-8")
        except:
            return
        db.sku = self.driver.find_element_by_css_selector("#content > article > div.product__right.md-6.md-right > div.product__propertyGroup > div.product__property.product__sku > span.product__propertyValue").text.encode("utf-8")
        # except:
			# db.sku = item
        db.cat = "|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("body > div.layout__container > aside.layout__top.layout__top--product > div > ul > li.nav__item")])
        try:
            db.desc =  self.driver.find_element_by_css_selector("#content > article > div.product__right.md-6.md-right > p").text.encode("utf-8")
        except:
            db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        try:
            db.size = self.driver.find_element_by_css_selector("div > div.product__property.product__dimensions > span.product__propertyValue").text.encode("utf-8")
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
        db.dir400 = "PBK400"
        db.dir160 = "PBK160"
        try:
            db.img400 = self.driver.find_element_by_css_selector("div > ul > li > a > img.zoomPanel__content").get_attribute("src")
        except:
            print "Image not detected."
            return
        db.img160 = db.img400.split("/")[-1:][0].split("?")[0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "PBK800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                # self.driver.find_element_by_css_selector("body > header > nav > ul > li:nth-child(2) > a").click()
                # self.time.sleep(1)
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
            items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#content > div > div.speedShop > div > article > figure > a")]
            return items
        except:
            return None

