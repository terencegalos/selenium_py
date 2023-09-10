from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class whiskey(domainobject.domainobject):

    vendor = "Whiskey Mountain"
    url = "http://www.whiskeymtn.com"
    home = "http://www.whiskeymtn.com"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("login[username]").send_keys(un)
        # self.driver.find_element_by_name("login[password]").send_keys(pw)
        # self.driver.find_element_by_name("login[password]").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#commerce > div > table > tbody > tr > td:nth-child(2) > table:nth-child(1) > tbody > tr:nth-child(1) > td > h1").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#ProductItemCode").text.encode("utf-8")
        db.cat = self.driver.find_element_by_css_selector("#commerce > div > div.BackToCategory > a").get_attribute("title").encode("latin-1")
        db.desc = self.driver.find_element_by_css_selector("#commerce > div > table > tbody > tr > td:nth-child(2) > table:nth-child(1) > tbody > tr:nth-child(2) > td > div > div.COMProdDesc.COMProdDescNoPrice").text.encode("utf-8")
        # db.stock = self.driver.find_element_by_css_selector("#commerce > div > table > tbody > tr > td:nth-child(2) > table:nth-child(1) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(3) > td:nth-child(2)").text.encode("utf-8")
        db.stock = self.driver.find_element_by_css_selector("#commerce > div > table > tbody > tr > td:nth-child(2) > table:nth-child(1) > tbody > tr:nth-child(2) > td > table > tbody > tr.OddRow > td:nth-child(2)").text.encode("utf-8")
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element_by_css_selector("#commerce > div > table > tbody > tr > td:nth-child(2) > table:nth-child(1) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td:nth-child(2)").text.encode("utf-8")
        db.seller = ""
        db.min1 = ""
        db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "Harv400"
        db.dir160 = "Harv160"
        db.img400 = (self.driver.find_element_by_css_selector("#COMProdImage").get_attribute("src")).replace("mn1_","lg1_")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Harv800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("SearchText").clear()
                self.driver.find_element_by_name("SearchText").send_keys(str(row))
                self.driver.find_element_by_name("SearchText").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                continue

        items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("div.COMSrchProdName > a")]
        return items

