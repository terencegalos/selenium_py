from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class p_crow_hollow(domainobject.domainobject):

    vendor = "Primitives_at_Crow_Hollow"
    url = "http://www.primitivesatcrowhollow.com/store/Default.asp"
    home = "http://www.primitivesatcrowhollow.com/store/Default.asp"
    uname = "service@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.driver.find_element_by_css_selector("#site > header > div > div > div.navigation > div > nav > ul:nth-child(2) > li:nth-child(3) > a").click()
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("email1").send_keys(un)
        self.driver.find_element_by_name("text1").send_keys(pw)
        self.driver.find_element_by_name("text1").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = WebDriverWait(self.driver,1.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body div center table tbody tr:nth-child(2) td:nth-child(2) div table tbody tr td p font table:nth-child(2) tbody tr td div:nth-child(5) center table tbody tr:nth-child(1) td:nth-child(2) p:nth-child(1) font"))).text.encode("utf-8")
            #db.name = self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div.ng-scope > div.row.ng-scope > div.col-xs-12.col-sm-5.col-md-5 > shopping-one-up-heading > div:nth-child(2) > div.col-xs-10 > p").text.encode("utf-8")
        except:
            return
        db.sku = ""
        db.cat = ""
        try:
            db.desc = self.driver.find_element_by_css_selector("body div center table tbody tr:nth-child(2) td:nth-child(2) div table tbody tr td p font table:nth-child(2) tbody tr td div:nth-child(5) center table tbody tr:nth-child(1) td:nth-child(2) font:nth-child(4)").text.encode("utf-8")
        except:
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
        db.dir400 = "Blossom400"
        db.dir160 = "Blossom160"
        self.driver.find_element_by_css_selector("body div center table tbody tr:nth-child(2) td:nth-child(2) div table tbody tr td p font table:nth-child(2) tbody tr td div:nth-child(5) center table tbody tr:nth-child(1) td:nth-child(1) p a").click()
        self.time.sleep(1)
		
        for h in self.driver.window_handles:
			self.driver.switch_to_window(h)
			db.img400 = self.driver.find_element_by_tag_name("img").get_attribute("src")
			self.driver.switch_to_default_content()
		
        db.img160 = db.img400.split("/")[-1:][0] if ".jpg?" not in db.img400.split("/")[-1:][0] else (db.img400.split("/")[-1:][0]).split("?")[0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Blossom800"
        db.img800 = db.img160     
        print db
        # if ".jpg" not in  db.img160:
            # return
        return db
        
        
    def search_item(self,row):
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("qrySearch").clear()
                self.driver.find_element_by_name("qrySearch").send_keys(row)
                self.driver.find_element_by_name("qrySearch").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        try:
			url = self.driver.find_element_by_css_selector("body div center table tbody tr:nth-child(2) td:nth-child(2) div table tbody tr td p font table:nth-child(1) tbody tr td table:nth-child(4) tbody tr td table tbody tr:nth-child(2) td a").get_attribute("href")
			print url
			return [url]
        except:
            return None

