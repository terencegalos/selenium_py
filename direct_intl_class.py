from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class direct_intl(domainobject.domainobject):

    vendor = "Direct_International"
    url = "http://directinternationalinc.com/"
    home = "http://directinternationalinc.com/"
    uname = "7261"
    passw = "N0G1A0"
    delay = 1
    item = None
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element_by_link_text("Log In").click()
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("u").send_keys(un)
        self.driver.find_element_by_name("p").send_keys(pw)
        self.driver.find_element_by_name("p").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        item = self.driver.find_element_by_css_selector("div.CONTENT div.bi.clearfix div.b div.bi.clearfix")
        db = gateway()
        try:
            db.name = item.find_element_by_css_selector("div.bt h2").text.encode("utf-8")
        except Exception as e:
            #raise e
            #return None
            print ""
        db.sku = item.find_element_by_css_selector("tr.sku td:nth-child(2)").text.encode("utf-8")
        try:
            db.cat = item.find_xpath("//*[@id=\"body\"]/div[2]/div/div/div/div[4]/div/div[2]/div/div[1]/div/h1")
        except:
            db.cat = ""
        db.desc = ""
        db.stock = item.find_element_by_css_selector("tr.status td:nth-child(2)").text.encode("utf-8")
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
            db.min1 = item.find_element_by_css_selector("tr.inner td:nth-child(2)").text.encode("utf-8")
        except:
            db.min1 = ""
        db.price1 = item.find_element_by_css_selector("tr.price td:nth-child(2)").text.encode("utf-8")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "directintl400"
        db.dir160 = "directintl160"
        db.img400 = (item.find_element_by_css_selector("img").get_attribute("src").replace("thumb","full"))
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "directintl800"
        db.img800 = db.img160     
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_css_selector("#searchfield").clear()
                self.driver.find_element_by_css_selector("#searchfield").send_keys(str(row))
                self.driver.find_element_by_css_selector("#searchfield").send_keys(self.Keys.ENTER)
                self.time.sleep(2)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        return None

