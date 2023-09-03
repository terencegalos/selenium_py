from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class toteable(domainobject.domainobject):

    vendor = "Capabunga Wine Products"
    url = "http://www.toteandable.com/index.php"
    home = "http://www.toteandable.com/index.php"
    login = "http://www.channelcraft.com/Wholesale-Login/"
    uname = "waresitat"
    passw = "wolfville"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#sw_dropdown_778 > a")).perform()
        # self.time.sleep(1)
        # print "Logging in..."
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(un)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(pw)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        # self.time.sleep(2)
        while True:
			try:
				db.name = self.driver.find_element_by_css_selector("#pdd-right > div.detailname > h1").text.encode("utf-8")
				break
			except:
				self.time.sleep(2)
				continue
        db.sku = self.driver.find_element_by_css_selector("#pdd-right > div.detailsku > span").text.encode("utf-8")
        db.cat = self.driver.find_element_by_css_selector("#ectform0 > div.prodnavigation.detailprodnavigation > a").text.encode("utf-8")
        try:
			db.desc = self.driver.find_element_by_css_selector("#pdd-right > div.detaildescription > p").text.encode("utf-8")
        except:
			db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""#self.driver.find_element_by_css_selector("#product-attribute-specs-table > tbody > tr.first.odd > td").text.encode("utf-8")
        db.seller = ""
        db.min1 = ""#self.driver.find_element_by_css_selector("#qty").get_attribute("value")
        db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "Capabunga400"
        db.dir160 = "Capabunga160"
        self.time.sleep(1)
        db.img400 = self.driver.find_element_by_css_selector("#zoom1").get_attribute("href")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        try:
			db.option = "|".join([o.text.encode("utf-8") for o in self.driver.find_elements_by_css_selector("#optn0x0 > option")])
        except:
			db.option = ""
        db.dir800 = "Capabunga800"
        db.img800 = db.img160
        print db
        # self.driver.back()
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("term").clear()
                self.driver.find_element_by_name("term").send_keys(row)
                self.driver.find_element_by_name("term").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                # self.driver.get(self.url)
                # self.time.sleep(1)
                continue
        try:
            item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#product > div > a")]
            print item
            return item
        except:
            return None