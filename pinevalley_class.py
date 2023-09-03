from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class pinevalley(domainobject.domainobject):

    vendor = "Pine Valley Pictures"
    url = "https://pinevalleypictures.com/"
    home = "https://pinevalleypictures.com/"
    login = "https://pinevalleypictures.com/"
    uname = "papas_candle_shoppe@papascandleshoppe.com"
    passw = "Vbills#54"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.login)
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
        db.name = self.driver.find_element_by_css_selector("#ProductSection > div.grid > div.grid-item.large--three-fifths > h1").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#ProductSection > div.grid > div.grid-item.large--three-fifths > h1").text.encode("utf-8").split("-")[0]
        db.cat = self.driver.find_element_by_css_selector("#ProductSection > div.grid > div.grid-item.large--three-fifths > p").text.encode("utf-8")
        db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element_by_css_selector("#ProductSection > div.grid > div.grid-item.large--three-fifths > div.product-description.rte > p").text.encode("utf-8")
        db.seller = ""
        db.min1 = ""#self.driver.find_element_by_css_selector("#qty").get_attribute("value")
        db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "Pine400"
        db.dir160 = "Pine160"
        self.time.sleep(1)
        db.img400 = self.driver.find_element_by_css_selector("div[id^=productPhotoWrapper-product-template] > div > img").get_attribute("srcset").split(",")[-1:][0].split()[0]
        db.img160 = db.img400.split("/")[-1:][0].split("?")[0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Pine800"
        db.img800 = db.img160
        print db
        self.driver.back()
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("q").clear()
                self.driver.find_element_by_name("q").send_keys(row)
                self.driver.find_element_by_name("q").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                # self.driver.get(self.url)
                # self.time.sleep(1)
                continue
        try:
            item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#shopify-section-search-template > div > div > div > div> a")]
            print item
            return item
        except:
            return None