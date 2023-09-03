from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class papascandles(domainobject.domainobject):

    vendor = "Papas Candle Shoppe"
    url = "https://www.papascandleshoppe.com/Default.asp"
    home = "https://www.papascandleshoppe.com/Default.asp"
    login = "https://www.papascandleshoppe.com/Default.asp"
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
        db.name = self.driver.find_element_by_css_selector("tbody > tr.vol-product__top__inner.vol-product__main-details__inner.clearfix > td.vol-product__top--right.col-xs-12.col-sm-8.col-sm-offset-2.col-md-offset-0.col-md-5 > font > span").text.encode("utf-8")
        # db.name = self.driver.find_element_by_css_selector("#product_addtocart_form > div.product-shop > div.product-name > h1").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("tbody > tr.vol-product__top__inner.vol-product__main-details__inner.clearfix > td.vol-product__top--right.col-xs-12.col-sm-8.col-sm-offset-2.col-md-offset-0.col-md-5 > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(1) > div > i > font > span.product_code").text.encode("utf-8")
        db.cat = "|".join([i.text for i in self.driver.find_elements_by_css_selector("tbody > tr:nth-child(1) > td > b > a")])
        db.desc = self.driver.find_element_by_css_selector("#product_description").text.encode("utf-8")
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
        db.dir400 = "Papas400"
        db.dir160 = "Papa160"
        self.time.sleep(1)
        db.img400 = self.driver.find_element_by_css_selector("#product_photo").get_attribute("src").split("?")[0]
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Papas800"
        db.img800 = db.img160
        print db
        self.driver.back()
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("Search").clear()
                self.driver.find_element_by_name("Search").send_keys(row)
                self.driver.find_element_by_name("Search").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                # self.driver.get(self.url)
                # self.time.sleep(1)
                continue
        try:
            item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#MainForm > table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > div > div > div > a")]
            print item
            return item
        except:
            return None