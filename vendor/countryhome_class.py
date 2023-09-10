from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class countryhome(domainobject.domainobject):

    vendor = "Country Home Creations"
    url = "https://countryhomecreations.com/"
    home = "https://countryhomecreations.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(5)
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
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("div.product__title__wrapper > h1").text.encode("utf-8")
        db.sku = item
        db.cat = ""
        try:
			db.desc = self.driver.find_element_by_css_selector("#shopify-section-product > div:nth-child(1) > div > div > div.grid__item.medium-up--one-half.product__form__wrapper > div.product__description.rte").text.encode("utf-8")
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
        db.dir400 = "CountryHome400"
        db.dir160 = "CountryHome160"
        try:
			db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#slick-slide00 > div > div > img"))).get_attribute("srcset").split(",")[-1:][0]
        except:
			db.img400 = "No/img"
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "CountryHome800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        self.driver.find_element_by_css_selector("#shopify-section-header > div > div > div.header--desktop.small--hide > nav > div.nav__search > a").click()
        self.time.sleep(1)
        while True:
            try:
                self.driver.find_element_by_name("q").clear()
                self.driver.find_element_by_name("q").send_keys(row)
                self.driver.find_element_by_name("q").send_keys(Keys.ENTER)
                break
            except Exception as e:
                print e
                self.driver.refresh()
                self.time.sleep(1)
                continue
        try:
            self.time.sleep(1)
            item = self.driver.find_element_by_css_selector("#MainContent > div > div > div > div.grid__item.five-sixths > p.h3--body > a").get_attribute("href")
            return [item]
        except:
            return None
