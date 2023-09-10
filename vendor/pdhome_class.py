from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class pdhome(domainobject.domainobject):

    vendor = "PD Home & Garden"
    url = "http://www.pdhomemarket.com/login.asp"
    home = "http://www.pdhomemarket.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        print "Logging in..."
        self.driver.find_element_by_name("email").send_keys(un)
        self.driver.find_element_by_name("password").send_keys(pw)
        self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = (self.driver.find_element_by_css_selector("#product_description").text.encode("utf-8")).replace(",","/comma")
        except:
            return
        db.sku = self.driver.find_element_by_css_selector("#v65-product-parent > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div > i > font > span.product_code").text.encode("utf-8")
        db.cat = "|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("#v65-product-parent > tbody > tr:nth-child(1) > td > b > a")])
        db.desc = self.driver.find_element_by_css_selector("#product_description").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element_by_css_selector("#v65-product-parent > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div").text.split("\n")[2]
        db.seller = ""
        db.min1 = self.driver.find_element_by_css_selector("#v65-productdetail-action-wrapper > table:nth-child(1) > tbody > tr > td:nth-child(1) > input").get_attribute("value")
        try:
			db.price1 = self.driver.find_element_by_css_selector("#v65-product-parent > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div > table > tbody > tr > td > font > div > b > span").get_attribute("content")
        except:
			return
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "PDHome400"
        db.dir160 = "PDHome160"
        try:
            db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#product_photo_zoom_url"))).get_attribute("href").split("?")[0]
        except:
            return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "PDHome800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("Search").clear()
                self.driver.find_element_by_name("Search").send_keys(row)
                self.driver.find_element_by_name("Search").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                continue
        
        try:
            item = self.driver.find_element_by_css_selector("div.v-product__details a").get_attribute("href")
            print item
            return [item]
        except Exception as e:
            print e
            return None
