from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class lighthouse(domainobject.domainobject):

    vendor = "Lighthouse Products"
    home = "https://www.lcpgifts.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.home)
        # self.driver.find_element_by_css_selector("#site > header > div > div > div.navigation > div > nav > ul:nth-child(2) > li:nth-child(3) > a").click()
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_css_selector("body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > modal > div.modal-body > modal-body > div.row.m-a-3 > div > login-fieldset > div:nth-child(1) > div > div > div:nth-child(1) > div > input").send_keys(un)
        # self.driver.find_element_by_css_selector("body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > modal > div.modal-body > modal-body > div.row.m-a-3 > div > login-fieldset > div:nth-child(2) > div > div > div:nth-child(1) > div > input").send_keys(pw)
        # self.driver.find_element_by_css_selector("body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > modal > div.modal-body > modal-body > div.row.m-a-3 > div > login-fieldset > div:nth-child(2) > div > div > div:nth-child(1) > div > input").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#content_asp_Repeater1_ProductTitleLabel_0").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#content_asp_Repeater1_ProductIDLabel_0").text.encode("utf-8")
        db.cat = "|".join([line.text.encode("utf-8") for line in self.driver.find_elements_by_css_selector("#site_path > a")])
        db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element_by_css_selector("#details > p.size").text.encode("utf-8")
        db.seller = ""
        db.min1 = ""
        db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "Lighthouse400"
        db.dir160 = "Lighthouse160"
        # db.img400 = self.driver.find_element_by_css_selector("#wrap > section:nth-child(2) > div > div > div > div:nth-child(3) > a").get_attribute("href")
        try:
            db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content_asp_Repeater1_Image1_0"))).get_attribute("src").split("?")[0].replace("medium","large")
        except:
            db.img400 = ""
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = self.driver.find_element_by_css_selector("#details > p.verse > a").text.encode("utf-8")
        db.option = ""
        db.dir800 = "Lighthouse800"
        db.img800 = db.img160
        print db
        # if ".jpg" not in  db.img160:
            # return
        return db
        
        
    def search_item(self,row):
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("ctl00$ctl07$txtSearchbar").send_keys(str(row))
                self.driver.find_element_by_name("ctl00$ctl07$txtSearchbar").send_keys(Keys.ENTER)
                self.time.sleep(self.delay)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(self.delay)
                continue

        return None

