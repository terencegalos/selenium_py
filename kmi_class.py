from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class kmi(domainobject.domainobject):

    vendor = "KMI International"
    url = "http://floralkmi.com/"
    uname = "waresitat"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in."
        # #expand login link btn
        # self.driver.find_element_by_css_selector("#navigation > div > div.col-xs-12.col-sm-12.col-md-4 > div > ul > li.header-account.dropdown.default-dropdown").click()
        # self.driver.click()
        # self.time.sleep(1)
        # self.driver.find_element_by_css_selector("#navigation > div > div.col-xs-12.col-sm-12.col-md-4 > div > ul > li.header-account.dropdown.default-dropdown.open > ul > li:nth-child(1) > a").click()
        # self.time.sleep(1)
        
        # self.driver.find_element_by_name("username").send_keys(un)
        # self.driver.find_element_by_name("password").send_keys(pw)
        # self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        try:
			db.name = self.driver.find_element_by_css_selector("body > div:nth-child(5) > div > div > div > div.details.col-md-6 > h3").text.encode("utf-8")
        except:
			db.name = ""
        db.sku = self.driver.find_element_by_css_selector("body > div:nth-child(5) > div > div > div > form > div > p:nth-child(3)").text.encode("utf-8")
        db.cat = ""
        db.desc = ""
        db.stock = ""
        db.set = ""
        db.custom = self.driver.current_url
        db.size = ""
        db.seller = ""
        db.min1 = 1
        db.price1 = 99
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "KMI400"
        db.dir160 = "KMI160"
        db.img400 = self.driver.find_element_by_css_selector("#pic_1 > a").get_attribute("href")
        print db.img400
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "KMI800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        # self.driver.get("https://floralkmi.com/index.php?option=com_virtuemart&view=category&virtuemart_category_id=0&virtuemart_manufacturer_id=0&Itemid=192")
        # self.time.sleep(1)
        try:
            self.driver.find_element_by_name("q").clear()
            self.driver.find_element_by_name("q").send_keys(str(row))
            self.driver.find_element_by_name("q").send_keys(self.Keys.ENTER)
        except:
            self.driver.find_element_by_name("productName").clear()
            self.driver.find_element_by_name("productName").send_keys(str(row))
            self.driver.find_element_by_name("productName").send_keys(self.Keys.ENTER)
        self.time.sleep(1)

        items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#listedproduct > div > form > div > h5 > a")]
        print items
        return items
        # return None

