from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class debry(domainobject.domainobject):

    vendor = "Debry Jewelry"
    url = "http://debrycompany.net/"
    home = "http://debrycompany.net/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # self.driver.find_element_by_css_selector("#pre-login-navbar > li.signIn-li > a").click()
        # self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("LogonEmail").send_keys(un)
        # self.driver.find_element_by_name("LogonPassword").send_keys(pw)
        # self.driver.find_element_by_name("LogonPassword").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        # db.name = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > h3").text.encode("utf-8")
        db.name = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > h3"))).text.encode("utf-8")
        db.sku = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > div.productDetail-item-pnumber > span:nth-child(2)"))).text.encode("utf-8")
        #db.sku = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > div.productDetail-item-pnumber > span:nth-child(2)").text.encode("utf-8")
        try:
            db.cat = self.driver.find_element_by_css_selector("#slick-container4 > div > div > div > div > div > div > div > div").text.encode("utf-8")
        except:
            db.cat = ""
        db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = ""
        db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "DCI400"
        db.dir160 = "DCI160"
        db.img400 = self.driver.find_element_by_css_selector("#product-detail-main-image").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "DCI800"
        db.img800 = db.img160     
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("s").clear()
                self.driver.find_element_by_name("s").send_keys(str(row))
                self.driver.find_element_by_name("s").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        try:
			item = self.driver.find_element_by_css_selector("")
        except:
            print "Search found nothing."
            return None

