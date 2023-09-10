from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

class dci(domainobject.domainobject):

    vendor = "Designs Combined"
    url = "https://shopdci.com/"
    home = "https://shopdci.com/Product"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element_by_css_selector("#pre-login-navbar > li.signIn-li > a").click()
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("LogonEmail").send_keys(un)
        self.driver.find_element_by_name("LogonPassword").send_keys(pw)
        self.driver.find_element_by_name("LogonPassword").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        while True:
            try:
                db.name = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > h3"))).text.encode("utf-8")
                break
            except:
                self.driver.refresh()
                time.sleep(6)
                continue
        db.sku = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > div.productDetail-item-pnumber > span:nth-child(2)"))).text.encode("utf-8")
        try:
            db.cat = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div.product-breadcrumb > a").text.encode("utf-8")
        except:
            db.cat = ""
        db.desc = ""
        try:
            db.stock = self.driver.find_element_by_css_selector("#product-qty-input-table > tbody > tr:nth-child(1) > td.status-image > ul > li:nth-child(1) > span:nth-child(2) > span").text.encode("utf-8")
        except:
            db.stock = self.driver.find_element_by_css_selector("div.product-item-discontinued > div > span").text.encode("utf-8")
            if "disc" in db.stock:
                return
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
            db.min1 = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > table.product-item-prices > tbody > tr:nth-child(1) > td.product-item-price.price-qty.text > span").text
        except:
            return 
        db.price1 = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > table.product-item-prices > tbody > tr:nth-child(1) > td:nth-child(1) > span:nth-child(1)").text
        try:
            db.min2 = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > table.product-item-prices > tbody > tr:nth-child(2) > td.product-item-price.price-qty.text > span").text
            db.price2 = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > table.product-item-prices > tbody > tr:nth-child(2) > td:nth-child(1) > span:nth-child(1)").text
        except:
            db.min2 = ""
            db.price2 = ""
        try:
            db.min3 = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > table.product-item-prices > tbody > tr:nth-child(3) > td.product-item-price.price-qty.text > span").text
            db.price3 = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > table.product-item-prices > tbody > tr:nth-child(3) > td:nth-child(1) > span:nth-child(1)").text
        except:
            db.min3 = ""
            db.price3 = ""
        db.multi = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > table.product-item-prices > tbody > tr:nth-child(1) > td.product-item-price.price-qty.text > span").text
        db.dir400 = "DCI400"
        db.dir160 = "DCI160"
        db.img400 = self.driver.find_element_by_css_selector("#product-detail-main-image").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > div.product-item-upc.margin-bottom-10 > table > tbody > tr > td.text.metrix").text
        db.option = ""
        db.dir800 = "DCI800"
        db.img800 = db.img160     
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_css_selector("#filter-searchString").clear()
                self.driver.find_element_by_css_selector("#filter-searchString").send_keys(str(row))
                self.driver.find_element_by_css_selector("#filter-searchString").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        # while True:
        try:
            btn  = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.product-item-item.hyperlink-like")))
            return [btn]
        except:
            return None
            # except:
            #     res = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-list-container div:nth-child(5) div"))).text
            #     if "No Products Found" in res:
            #         print "Item not found."
            #         break

