from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class barncat(domainobject.domainobject):

    vendor = "Barn Cat Mercantile"
    url = "https://barncatmercantile.com/"
    home = "https://barncatmercantile.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#sw_dropdown_2878 > a")).perform()
        # self.time.sleep(1)
        # self.driver.find_element_by_css_selector("#sw_dropdown_2878 > a").click()
        # self.time.sleep(1)
        # self.driver.find_element_by_css_selector("#account_info_2878 > div.ty-account-info__buttons.buttons-container > a.cm-dialog-opener.cm-dialog-auto-size.ty-btn.ty-btn__secondary").click()
        
        # self.time.sleep(1)
        # print "Logging in..."
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "user_login"))).send_keys(un)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(pw)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(Keys.ENTER)
        # self.time.sleep(3)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = (self.driver.find_element_by_css_selector("#ProductSection > div.product-single > div > div:nth-child(2) > h1").text.encode("utf-8"))
        db.sku = ""
        db.cat = ""
        try:
			db.desc = self.driver.find_element_by_css_selector("#description > div").text.encode("utf-8")
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
        db.dir400 = "Barncat400"
        db.dir160 = "Barncat160"
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#fancybox-wrap")).perform()
        # self.time.sleep(1)
        try:
			db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ProductSection > div.product-single > div > div:nth-child(1) > div div img"))).get_attribute("srcset")
        except:
			db.img400 = "No/img"
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Barncat800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                try:
                    self.driver.find_element_by_name("q").clear()
                except:
                    self.driver.find_element_by_name("hint_q").clear()
                try:
                    self.driver.find_element_by_name("q").send_keys(row)
                except:
                    self.driver.find_element_by_name("hint_q").send_keys(row)
                try:
                    self.driver.find_element_by_name("q").send_keys(Keys.ENTER)
                except:
                    self.driver.find_element_by_name("hint_q").send_keys(Keys.ENTER)
                break
            except Exception as e:
                print e
                self.driver.refresh()
                self.time.sleep(1)
                continue
        try:
            self.time.sleep(1)
            item = self.driver.find_element_by_css_selector("a.product-title").get_attribute("href")
            return [item]
        except:
            return None
