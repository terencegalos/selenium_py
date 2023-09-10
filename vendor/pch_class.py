from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class pch(domainobject.domainobject):

    vendor = "Primitives at Crow Hollow"
    url = "http://www.primitivesatcrowhollow.com/store/Default.asp"
    home = "http://www.primitivesatcrowhollow.com/store/Default.asp"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#sw_dropdown_778 > a")).perform()
        # self.time.sleep(1)
        print "Logging in..."
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login[username]"))).send_keys(un)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login[password]"))).send_keys(pw)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login[password]"))).send_keys(Keys.ENTER)
        # self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("body > div > center > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > p > font > table:nth-child(2) > tbody > tr > td > div:nth-child(5) > center > table > tbody > tr:nth-child(1) > td:nth-child(2) > p:nth-child(1) > font").text.encode("utf-8")
        db.sku = db.name.split()[1]
        db.cat = ""
        db.desc = self.driver.find_element_by_css_selector("body > div > center > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > p > font > table:nth-child(2) > tbody > tr > td > div:nth-child(5) > center > table > tbody > tr:nth-child(1) > td:nth-child(2) > font:nth-child(4)").text.encode("utf-8")
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
        db.dir400 = "PrimitiveCrow400"
        db.dir160 = "PrimitiveCrow160"
        self.time.sleep(1)
        db.img400 = "http://www.primitivesatcrowhollow.com/fpdb/images/" + WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div > center > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > p > font > table:nth-child(2) > tbody > tr > td > div:nth-child(5) > center > table > tbody > tr:nth-child(1) > td:nth-child(1) > p > a > img"))).get_attribute("src").split("=")[-1:][0]
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = "|".join(i.text.encode("utf-8") for i in self.driver.find_elements_by_tag_name("option"))
        db.dir800 = "PrimitiveCrow800"
        db.img800 = db.img160
        print db
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
                self.driver.refresh()
                continue
        try:
            item = self.driver.find_element_by_css_selector("body > div > center > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > p > font > table:nth-child(1) > tbody > tr > td > table:nth-child(4) > tbody > tr > td > table > tbody > tr:nth-child(1) > td > a").get_attribute("href")
            print item
            return [item]
        except:
            return None
