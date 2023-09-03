from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class cbd(domainobject.domainobject):

    vendor = "CBD Body Blends"
    url = "https://cbdbodyblends.com/"
    home = "https://cbdbodyblends.com/"
    uname = "service@waresitat.com"
    passw = "Wolfville1"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element_by_css_selector("#top-bar > div > div.flex-col.hide-for-medium.flex-right > ul > li.account-item.has-icon > a").click()
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#sw_dropdown_778 > a")).perform()
        # self.time.sleep(1)
        print "Logging in..."
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(un)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(pw)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(Keys.ENTER)
        # self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#maincontent > div.page-title-wrapper.product > h1 > span").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#maincontent > div.columns > div > div.product-info-main > div.product-info-price > div.product-info-stock-sku > div.product.attribute.sku > div").text.encode("utf-8")
        db.cat = ""
        try:
			db.desc = self.driver.find_element_by_css_selector("#description > div > div").text.encode("utf-8")
        except:
			db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        try:
			db.size = self.driver.find_element_by_css_selector("#product-attribute-specs-table > tbody > tr.first.odd > td").text.encode("utf-8")
        except:
			db.size = ""
        db.seller = ""
        try:
			db.min1 = self.driver.find_element_by_css_selector("#qty").get_attribute("value")
        except:
			db.min1 = ""
        db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "rowepottery400"
        db.dir160 = "rowepottery160"
        self.time.sleep(4)
        db.img400 = self.driver.find_element_by_css_selector("#maincontent > div.columns > div > div.product.media img.fotorama__img").get_attribute("src")
        print db.img400
        # db.img400 = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.NAME, "div > img.fotorama__img"))).get_attribute("src")
        # print db.img400
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "rowepottery800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_css_selector("#masthead > div.header-inner.flex-row.container.logo-left.medium-logo-center > div.flex-col.hide-for-medium.flex-right > ul > li.header-search.header-search-lightbox.has-icon > a").click()
				
                self.driver.find_element_by_name("s").clear()
                self.driver.find_element_by_name("s").send_keys(row)
                self.driver.find_element_by_name("s").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                continue
        try:
            item = [a.get_attribute("href") for a in  self.driver.find_elements_by_css_selector("#maincontent > div.columns > div > div.search.results > div.products.wrapper.list.products-list > ol > li > div > div > strong > a")]
            print item
            return item
        except:
            return None