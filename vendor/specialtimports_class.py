from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class specialt(domainobject.domainobject):

    vendor = "Special T Imports"
    url = "https://sti.specialtimports.com/Products"
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

    def save_info(self,obj=None):
        db = gateway()
        db.name = obj.find_element_by_css_selector("p:nth-child(3)").text.encode("utf-8")
        db.sku = obj.find_element_by_css_selector("strong.text-dark").text.encode("utf-8")
        db.cat = ""
        db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = obj.find_element_by_css_selector("p:nth-child(3)").text.encode("utf-8").splitlines()[-1]
        db.seller = ""
        db.min1 = 1
        db.price1 = 1
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "specialtimports400"
        db.dir160 = "specialtimports160"
        db.img400 = obj.find_element_by_css_selector(".img-fluid").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "specialtimports800"
        db.img800 = db.img160
        # print db
        return db

    def get_info(self,item=None):
        dbs = []
        result = self.driver.find_elements_by_css_selector("div.text-center")
        for res in result:
            data = self.save_info(res)
            dbs.append(data)
        return dbs
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        # if len(row.split(",")[1].strip()) > 1:
        while True:
            try:
                self.driver.find_element_by_id("searchTags").clear()
                self.driver.find_element_by_id("searchTags").send_keys(row)
                self.driver.find_element_by_id("searchTags").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except Exception as e:
                print "Search fail:"
                print e
                self.driver.refresh()
                self.time.sleep(1)
                continue
        # try:
        #     items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector(".img-prod")]
        #     return items
        # except:
            return None
            

