from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class channelcraft(domainobject.domainobject):

    vendor = "Channel Craft"
    url = "http://channelcraft.com/Scripts/PublicSite/"
    home = "http://channelcraft.com/Scripts/PublicSite/"
    login = "http://www.channelcraft.com/Wholesale-Login/"
    uname = "waresitat"
    passw = "wolfville"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.login)
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#sw_dropdown_778 > a")).perform()
        # self.time.sleep(1)
        print "Logging in..."
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(un)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(pw)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#popupwrapper > table > tbody > tr:nth-child(1) > td > strong").text.encode("utf-8")
        # db.name = self.driver.find_element_by_css_selector("#product_addtocart_form > div.product-shop > div.product-name > h1").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#descCell > p.sku").text.encode("utf-8").split()[-1:][0]
        db.cat = ""
        db.desc = self.driver.find_element_by_css_selector("#descCell > p.desc").text.encode("utf-8")
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
        db.dir400 = "Channel400"
        db.dir160 = "Channel160"
        self.time.sleep(1)
        db.img400 = self.driver.find_element_by_css_selector("#imgCell > img").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Channel800"
        db.img800 = db.img160
        print db
        self.driver.back()
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