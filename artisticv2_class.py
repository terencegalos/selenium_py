from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class artisticv2(domainobject.domainobject):

    vendor = "Artistic_Reflections"
    url = "http://www.artisticreflections.com/login.asp"
    home = "http://www.northamericanart.com"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.home)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("email").send_keys(un)
        # self.driver.find_element_by_name("password").send_keys(pw)
        # self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = ""
        db.sku = self.driver.find_element_by_css_selector("#v65-product-parent > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div > i > font > span.product_code").text.encode("utf-8")
        db.cat = "|".join([c.text.encode("utf-8") for c in self.driver.find_elements_by_css_selector("#v65-product-parent > tbody > tr:nth-child(1) > td > b > a")])
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
        db.dir400 = "NorthAmerican400"
        db.dir160 = "NorthAmerican160"
        # db.img400 = self.driver.find_element_by_css_selector("#MainForm > table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(1) > td:nth-child(1) > a > img").get_attribute("src")
        # db.img400 = self.driver.find_element_by_css_selector("#vZoomArea > img").get_attribute("src")
        try:
			db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#product_photo_zoom_url2"))).get_attribute("href")
        except:
			db.img400 = "No/image."
        # db.img400 = self.driver.find_element_by_css_selector("#vZoomMagnifierImage").get_attribute("src")
        if "nophoto" in db.img400:
            print "No photo detected..."
            return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "NorthAmerican800"
        db.img800 = db.img160     
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        # while True:
            # try:
        self.driver.find_element_by_name("Search").clear()
        self.driver.find_element_by_name("Search").send_keys(str(row))
        self.driver.find_element_by_name("Search").send_keys(Keys.ENTER)
        self.time.sleep(1)
                # break
            # except:
                # self.driver.get(self.home)
                # self.time.sleep(1)
                # continue

        try:
            item = self.driver.find_element_by_css_selector("#MainForm > table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > div > a").get_attribute("href")
            return [item]
        except:
            return

