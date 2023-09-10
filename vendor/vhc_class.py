from table_gateway import gateway
import domainobject
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class vhc(domainobject.domainobject):

    vendor = "VHC_Brands_(Victorian_Heart)"
    url = "http://vhcbrands.com/"
    home = "http://vhcbrands.com/"
    uname = "waresitat"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("username").send_keys(un)
        # self.driver.find_element_by_name("password").send_keys(pw)
        # self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        while True:
            try:
                db = gateway()
                db.name = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-detail > div > article > section.item-details-main-content > div.item-details-content-header > h1"))).text.encode("utf-8")
                try:
                    db.sku = self.driver.find_element_by_css_selector("#product-detail > div > article > section.item-details-main-content > div.item-details-main > div.item-details-options-id > span.item-details-sku-value").text.encode("utf-8")
                except:
                    db.sku = ""
                db.cat = ""
                try:
                    db.desc = self.driver.find_element_by_css_selector("#product-detail > div > article > section.item-details-more-info-content > div.item-details-more-info-content-container > div:nth-child(2) > div").text.encode("utf-8")
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
                db.dir400 = "VHC400"
                db.dir160 = "VHC160"
                # db.img400 = self.driver.find_element_by_css_selector("#product-detail > div > article > section.item-details-main-content > div.item-details-image-gallery-container > div:nth-child(2) > div > div img:nth-child(1)").get_attribute("src").split("?")[0]
                db.img400 = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-detail > div > article > section.item-details-main-content > div.item-details-image-gallery-container > div:nth-child(2) > div > div img:nth-child(1)"))).get_attribute("src").split("?")[0]
                db.img160 = db.img400.split("/")[-1:][0]
                db.desc2 = ""
                db.option = ""
                db.dir800 = "VHC800"
                db.img800 = db.img160     
                print db
                return db
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                continue
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        
        while True:
            try:
                self.driver.find_element_by_css_selector("#site-header > div.header-secondary-section > div.header-menu-search > button").click()
                self.time.sleep(1)
                self.driver.find_elements_by_css_selector("#site-header > div.header-secondary-section > div.header-site-search input")[1].send_keys(row.rstrip())
                self.time.sleep(1)
                item = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#site-header > div.header-secondary-section > div.header-site-search > div > div > form > div > div > span > span a")))
                break
            except:
                self.driver.get(self.url)
                self.time.sleep(1)
                continue
        
        try:
            return [item]
        except:
            return None


