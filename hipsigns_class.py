from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class hipsigns(domainobject.domainobject):

    vendor = "Hip Signs for Cool Folks"
    url = "http://www.lorriepowellstudios.com/index.html"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("Customer_LoginEmail").send_keys(un)
        # self.driver.find_element_by_name("Customer_Password").send_keys(pw)
        # self.driver.find_element_by_name("Customer_Password").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element_by_css_selector("#topcap > img:nth-child(1)").text.encode("utf-8")
        except:
            return
        try:
            body = self.driver.find_element_by_css_selector("#shopp").text.encode("utf-8").splitlines()
            if len(body) < 1:
                raise
        except:
            body = self.driver.find_element_by_css_selector("body > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr > td:nth-child(3) > table > tbody > tr:nth-child(3)").text.encode("utf-8").splitlines()
        print body
        db.sku = body[0]
        db.cat = ""
        # db.desc = self.driver.find_element_by_css_selector("#shopp > p:nth-child(5)").text.encode("utf-8")
        db.desc = body[-1]
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
            db.min1 = self.driver.find_element_by_css_selector("#shopp > form select option:nth-child(1)").get_attribute("value")
        except:
            db.min1 = "Out of stock"

        try:
            db.price1 = self.driver.find_element_by_css_selector(".price").text.encode("utf-8")
        except:
            return None
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "Paine"
        db.dir160 = "Paine"
        try:
            db.img400 = self.driver.find_element_by_css_selector(".prodimg").get_attribute("src")
        except:
            db.img400 = "No/noimage"
            
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Paine"
        db.img800 = db.img160
        print db
        return db

    
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
        

    def nextPage(self):
        try:
            self.driver.find_element_by_css_selector("div.alignright:nth-child(3) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(4) > span:nth-child(1) > a:nth-child(1)").click()
            self.time.sleep(1)
            print "More pages***"
            return True
        except:
            print "Exhausted***"
            return False

    def get_nav_links(self):
        
        l = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#e1 > table > tbody > tr > td > a")]
        print(*l,sep = ", ")
        return l

    def _initScraper(self):

        links = get_nav_links()
        for link in links:
            self.driver.get(link)
            self.time.sleep(1)

            print links