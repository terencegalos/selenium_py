from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class chc(domainobject):

    vendor = "Country Home Creations"
    url = "https://countryhomecreations.com/"
    home = "https://countryhomecreations.com/"
    uname = "kaye.williams@waresitat.com"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # self.driver.find_element(By.CSS_SELECTOR,"#external_links > ul.hidden-xs.nav.navbar-nav.navbar-right > li:nth-child(2) > a > span > i").click()
        # self.time.sleep(1)
        # self.driver.find_element(By.CSS_SELECTOR,"#external_links > ul.hidden-xs.nav.navbar-nav.navbar-right > li.dropdown-grid.no-open-arrow.open > div > div > div > div.login_frm > div > a:nth-child(1)").click()
        # self.time.sleep(1)
        
        # try:
        # print "Logging in..."
# self.driver.  find_element(By.NAME,'customer[email]').send_keys(un)
        # self.driver.find_element(By.NAME,'customer[password]').send_keys(pw)
        # self.driver.find_element(By.NAME,'customer[password]').send_keys(Keys.ENTER)
        # driver.find_element(By.CSS_SELECTOR,"#customer_login > div.row > div.col-sm-5.col-ms-6.col-xs-4 > p > input").click()
        print("Login Success.")
        self.time.sleep(1)
        # except:
            # print "Login failed."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element(By.CSS_SELECTOR,"#MainContent > section:nth-child(1) > section > div > div.product__info-wrapper.grid__item.scroll-trigger.animate--slide-in > product-info > div.product__title > h1").text.encode("utf-8")
        db.sku = item#json.loads(self.driver.find_element(By.CSS_SELECTOR,"#shopify-section-product > div:nth-child(1) > script").text)["sku"]
        # except:
			# db.sku = item
        db.cat = ""
        try:
            db.desc =  self.driver.find_element(By.CSS_SELECTOR,"#MainContent > section:nth-child(1) > section > div > div.product__info-wrapper.grid__item.scroll-trigger.animate--slide-in > product-info > div.product__description.rte.quick-add-hidden > p:nth-child(1)").text.encode("utf-8")
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
        db.img400 = "https"+self.driver.find_element(By.CSS_SELECTOR,"#MainContent > section:nth-child(1) > section > div > div.grid__item.product__media-wrapper > media-gallery > slider-component > ul > li > div > modal-opener > div.product__media.media.media--transparent > img").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "CountryHome800"
        db.img800 = db.img160
        print(db)
        return db
        
        
    def search_item(self,row):
        print("\nSearching for item: " + row+"\n")
        # time.sleep(999)
        self.driver.find_element(By.CSS_SELECTOR,"body > div.shopify-section.shopify-section-group-header-group.section-header.shopify-section-header-sticky > sticky-header > header > details-modal > details > summary > span > svg.modal__toggle-open.icon.icon-search").click()
        self.time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR,"#Search-In-Modal-1").clear()
        self.driver.find_element(By.CSS_SELECTOR,"#Search-In-Modal-1").send_keys(str(row))
        self.driver.find_element(By.CSS_SELECTOR,"#Search-In-Modal-1").send_keys(self.Keys.ENTER)
        self.time.sleep(1)
        try:
            item = self.driver.find_element(By.CSS_SELECTOR,"#product-grid > ul > li > div > div > div.card__content > div.card__information > h3 > a").get_attribute("href")
            print(item)
            return [item]
        except:
            return None

