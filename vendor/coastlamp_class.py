from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class coastlamp(domainobject.domainobject):

    vendor = "Coast Lamp Mfg"
    url = "http://www.coastlampmfg.com/ProductParameters?method=&filter_Collection=CASUAL+LIVING+COLLECTION&filter_Main+Category=&search="
    home = "http://www.coastlampmfg.com/ProductParameters?method=&filter_Collection=CASUAL+LIVING+COLLECTION&filter_Main+Category=&search="
    login = "https://pinevalleypictures.com/"
    uname = "papas_candle_shoppe@papascandleshoppe.com"
    passw = "Vbills#54"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # self.driver.find_element_by_css_selector("body > article > section > div > header > div.header__section > div > div > div.col-xs-3.microblock-group.text-right.no-pad-left-xs > a").click()
        # self.time.sleep(1)
        # print "Logging in..."
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(un)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(pw)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#products > div > div > form > div > div > h3").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#products > div > div > form > div > div > div.backpage > table > tbody > tr:nth-child(2) > td:nth-child(1) > span").text.encode("utf-8")
        db.cat = self.driver.find_element_by_css_selector("#products > div > div > form > div > div > div.backpage > div.footnotes > table > tbody > tr > td:nth-child(1) > span:nth-child(2)").text.encode("utf-8")
        db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element_by_css_selector("#products > div > div > form > div > div > div.backpage > div.footnotes > table > tbody > tr > td:nth-child(1) > span:nth-child(11)").text.encode("utf-8")
        db.seller = ""
        db.min1 = ""
        db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "Coast400"
        db.dir160 = "Coast160"
        self.time.sleep(1)
        db.img400 = self.driver.find_element_by_css_selector("#products > div > div > form > div > div > div.frontpage > img").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0].split("?")[0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Coast800"
        db.img800 = db.img160
        print db
        self.driver.back()
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("search").clear()
                self.driver.find_element_by_name("search").send_keys(row)
                self.driver.find_element_by_name("search").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                # self.driver.get(self.url)
                # self.time.sleep(1)
                continue
        try:
            item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#products > div > div > form > div > div.ChicagoGrid > div > a")]
            print item
            return item
        except:
            return None