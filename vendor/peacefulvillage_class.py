from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class peacefulvillage(domainobject.domainobject):

    vendor = "Peaceful Village Jewelry"
    url = "http://www.peacefulvillage.com/"
    last = "http://www.peacefulvillage.com/shop/a-jewelery-sets/p-n-a040pus/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    links = []
    flag = 0
    skus = []
    all = []
        
    def nextPage(self):
        try:
            self.driver.find_element_by_css_selector("a.next").click()
            self.time.sleep(1)
            return True
        except:
            print "Page exhausted."
            self.time.sleep(1)
            return False

    def init_login(self,un,pw):
        self.driver.get("http://www.peacefulvillage.com/my-account/")
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("username").send_keys(un)
        self.driver.find_element_by_name("password").send_keys(pw)
        self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element_by_css_selector("div.summary.entry-summary > div:nth-child(3) > p:nth-child(1)").text.encode("utf-8")
        except:
            return
        db.sku = self.driver.find_element_by_css_selector("div.summary.entry-summary > h1").text.encode("utf-8")
        db.cat = self.driver.current_url
        db.desc = self.driver.find_element_by_css_selector("div.summary.entry-summary > div:nth-child(3) > p:nth-child(1)").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
            db.min1 = [line for line in self.driver.find_element_by_css_selector("div.summary.entry-summary > div:nth-child(3)").text.splitlines() if "min" in line.lower()][0].text.encode("utf-8")
        except:
            db.min1 = self.driver.find_element_by_css_selector("div.summary.entry-summary > form > div > input.input-text.qty.text").get_attribute("value")

        db.price1 = self.driver.find_element_by_css_selector("p[itemprop='price'] > span").text.encode("utf-8")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "Peaceful400"
        db.dir160 = "Peaceful160"
        db.img400 = self.driver.find_element_by_css_selector("div.images > a").get_attribute("href")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Peaceful800"
        db.img800 = db.img160
        print db
        return db

        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        # if len(row.split(",")[1].strip()) > 1:
        while True:
            try:
                self.driver.find_element_by_name("s").clear()
                self.driver.find_element_by_name("s").send_keys(row)
                self.driver.find_element_by_name("s").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except Exception as e:
                print "Search fail:"
                print e
                self.driver.refresh()
                self.time.sleep(1)
                continue

        try:
            items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#main > ul > li > a") if i.get_attribute("href") not in self.links]
            # sku = [i.text for i in self.driver.find_elements_by_css_selector("#main > ul > li > a > h3") if i.text not in self.skus]
            print items
            self.links.extend(items)
            self.skus.extend(sku)
            while self.nextPage():
                items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#main > ul > li > a") if i.get_attribute("href") not in self.links]
                # sku = [i.text for i in self.driver.find_elements_by_css_selector("#main > ul > li > a > h3") if i.text not in self.skus]
                print items
                self.skus.extend(sku)
                self.links.extend(items)

            # print self.skus
            # self.time.sleep(20)
            return self.links
        except:
            return None
            

