from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class vipsale(domainobject.domainobject):

    vendor = "VIP Home & Garden Discount Closeouts"
    url = "http://viphomeandgarden.com/"
    home = "http://viphomeandgarden.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        # self.driver.find_element_by_css_selector("#site > header > div > div > div.navigation > div > nav > ul:nth-child(2) > li:nth-child(3) > a").click()
        # self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_css_selector("body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > modal > div.modal-body > modal-body > div.row.m-a-3 > div > login-fieldset > div:nth-child(1) > div > div > div:nth-child(1) > div > input").send_keys(un)
        # self.driver.find_element_by_css_selector("body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > modal > div.modal-body > modal-body > div.row.m-a-3 > div > login-fieldset > div:nth-child(2) > div > div > div:nth-child(1) > div > input").send_keys(pw)
        # self.driver.find_element_by_css_selector("body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > modal > div.modal-body > modal-body > div.row.m-a-3 > div > login-fieldset > div:nth-child(2) > div > div > div:nth-child(1) > div > input").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#product-header-row > h1").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#product > div.medium-6.columns.logged-out > h5").text.encode("utf-8")
        db.cat = ""
        db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element_by_css_selector("#product > div.medium-6.columns.logged-out > p").text.encode("utf-8")
        db.seller = ""
        db.min1 = ""
        db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "VIP400"
        db.dir160 = "VIP160"
        try:
            db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main-img"))).get_attribute("src").split("?")[0]
        except:
            db.img400 = ""
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "VIP800"
        db.img800 = db.img160
        print db
        # if ".jpg" not in  db.img160:
            # return
        return db
        
        
    def search_item(self,row):
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                # self.driver.find_element_by_css_selector("#menu > li.search").click()
                # self.time.sleep(0.5)
                self.driver.find_element_by_name("q").send_keys(str(row))
                self.driver.find_element_by_name("q").send_keys(Keys.ENTER)
                self.time.sleep(self.delay)
                break
            except:
                self.driver.get(self.url)
                self.time.sleep(self.delay)
                continue

        try:
            item = self.driver.find_element_by_css_selector("#results > div > div > a").get_attribute("href")
            print item
            return [item]
        except:
            return None

