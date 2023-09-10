from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class desma(domainobject.domainobject):

    vendor = "Desma Group Home & Gift"
    url = "http://desma-group.com/customer/account/login/"
    home = "http://desma-group.com/customer/account/login/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#sw_dropdown_778 > a")).perform()
        # self.time.sleep(1)
        print "Logging in..."
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login[username]"))).send_keys(un)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login[password]"))).send_keys(pw)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login[password]"))).send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element_by_css_selector("#item-contenttitle").text.encode("utf-8")
        except:
            db.name = self.driver.find_element_by_css_selector("#product_addtocart_form > div.product-essential > div.summary").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#product_addtocart_form > div.product-essential > p").text.encode("utf-8")
        db.cat = ""
        db.desc = self.driver.find_element_by_css_selector("#product-attribute-specs-table > tbody").text.encode("utf-8")
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
        db.dir400 = "desma400"
        db.dir160 = "desma160"
        self.time.sleep(1)
        #db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#fancybox-img"))).get_attribute("src")
        db.img400 = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#image1"))).get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = "|".join(i.text.encode("utf-8") for i in self.driver.find_elements_by_tag_name("option"))
        db.dir800 = "desma800"
        db.img800 = db.img160
        print db
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
                continue
        try:
            item = [[i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("body > div > div.main > div.rightlist > div.category-products > ul > li > p.title > a")][0]]
            return item
        except:
            return None
