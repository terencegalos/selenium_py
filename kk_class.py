from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class kk(domainobject.domainobject):

    vendor = "K&K_Interiors"
    url = "https://www.kkinteriors.com/login"
    home = "https://www.kkinteriors.com"
    uname = "service@waresitat.com"
    passw = "wolfville"
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_id("Username").send_keys(un)
        self.driver.find_element_by_id("Password").send_keys(pw)
        self.driver.find_element_by_id("Password").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = "No name"
        db.sku = WebDriverWait(self.driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#productnumbertext"))).text.encode("utf-8")
        db.cat = "|".join([c.text for c in self.driver.find_elements_by_css_selector("#product-detail-spreads h1")])
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
        db.dir400 = "K&K400"
        db.dir160 = "K&K160"
        db.img400 = self.driver.find_element_by_css_selector("#productimage").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "K&K800"
        db.img800 = db.img160     
        print db
        if ".jpg" not in  db.img160:
            return
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_id("search_box").clear()
                self.driver.find_element_by_id("search_box").send_keys(str(row))
                self.driver.find_element_by_id("search_box").send_keys(self.Keys.ENTER)
                self.time.sleep(2)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        try:
            WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,"productimage"))).click()
            self.time.sleep(1)
            return
        except:
            return None

