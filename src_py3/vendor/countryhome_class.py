from helper.table_gateway import gateway
from helper.domainobject import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json

class countryhome(domainobject):

    vendor = "Country Home Creations"
    url = "https://countryhomecreations.com/"
    home = "https://countryhomecreations.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1

    def __init__(self,driver,mode):
        super().__init__(driver)
        self.mode = mode
        self.links = []
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(5)
        # ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#sw_dropdown_2878 > a")).perform()
        # self.time.sleep(1)
        # self.driver.find_element(By.CSS_SELECTOR,"#sw_dropdown_2878 > a").click()
        # self.time.sleep(1)
        # self.driver.find_element(By.CSS_SELECTOR,"#account_info_2878 > div.ty-account-info__buttons.buttons-container > a.cm-dialog-opener.cm-dialog-auto-size.ty-btn.ty-btn__secondary").click()
        
        # self.time.sleep(1)
        # print "Logging in..."
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "user_login"))).send_keys(un)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(pw)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(Keys.ENTER)
        # self.time.sleep(3)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element(By.CSS_SELECTOR,"#MainContent > section:nth-child(1) > section > div > div.product__info-wrapper.grid__item.scroll-trigger.animate--slide-in > product-info > div.product__title > h1").text

        els = self.driver.find_elements(By.XPATH,"//script[@type='application/ld+json']")
        text = [el.get_attribute("innerHTML") for el in els if 'sku' in el.get_attribute("innerHTML").lower()][0]
        jsn = json.loads(text)
        print(jsn.items())
        
        db.sku = jsn['sku']

        db.cat = ""
        try:
            db.desc = self.driver.find_element(By.CSS_SELECTOR,"#MainContent > section:nth-child(1) > section > div > div.product__info-wrapper.grid__item.scroll-trigger.animate--slide-in > product-info > div.product__description.rte.quick-add-hidden").text
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
            # db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#Slide-template--16812176441594__main-32961851982074 > div > modal-opener > div.product__media.media.media--transparent > img"))).get_attribute("srcset").split(",")[-1:][0]
            db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#MainContent > section:nth-child(1) > section > div > div.grid__item.product__media-wrapper > media-gallery > slider-component:nth-child(2) > ul > li.product__media-item.grid__item.slider__slide.is-active.scroll-trigger.animate--fade-in > div > modal-opener > div.product__media.media.media--transparent > img"))).get_attribute("srcset").split(",")[-1:][0]
        except:
            db.img400 = "No/img"
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "CountryHome800"
        db.img800 = db.img160
        print(db)
        return db
        
        
    def search_item(self,row):
        
        print("\nSearching for item: " + row+"\n")
        self.driver.find_element(By.CSS_SELECTOR,"body > div.shopify-section.shopify-section-group-header-group.section-header.shopify-section-header-sticky > sticky-header > header > details-modal > details > summary > span").click()
        # self.time.sleep(1)
        while True:
            try:
                self.driver.find_element(By.NAME,"q").clear()
                self.driver.find_element(By.NAME,"q").send_keys(row)
                self.driver.find_element(By.NAME,"q").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            except Exception as e:
                print(e)
                self.driver.refresh()
                self.time.sleep(1)
                continue
        try:
            item = self.driver.find_element(By.XPATH,"//*[@id='product-grid']/ul/li/div/div/div[2]/div[1]/h3/a").get_attribute("href")
            print(item)
            return [item]
        except:
            return None
