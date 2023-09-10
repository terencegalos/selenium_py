from table_gateway import gateway
import domainobject
import xmltodict
import requests

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class warmglow(domainobject.domainobject):

    # sitemap = "https://warmglow.com/product-sitemap.xml"
    sitemap = "https://warmglow.com/wp-sitemap-posts-product-1.xml"
    vendor = "Warm Glow Candles"
    url = "https://warmglow.com/"
    home = "https://warmglow.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
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

    def isBtn(self):
        if len(self.driver.find_elements_by_css_selector("#fragrance > option")) > 2:
            return True
        else:
            return False

    def clickBtn(self):
        ls = []
        btn = self.driver.find_elements_by_css_selector("#fragrance > option")
        for x,b in enumerate(btn):
            try: # use try except if btn goes stale
                b.click()
            except:
                b = self.driver.find_elements_by_css_selector("#fragrance > option")[x]
                b.click()
            self.time.sleep(1)
            ls.append(self.get_info())
        return ls

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element_by_css_selector("div.summary.entry-summary > h1").text.encode("utf-8")
        except:
            return None
        db.sku = db.name
        db.cat = ""
        try:
			db.desc = self.driver.find_element_by_css_selector("div.summary.entry-summary > div.woocommerce-product-details__short-description > p").text.encode("utf-8")
        except:
			db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = 1
        db.price1 = 99
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "WarmGlow400"
        db.dir160 = "WarmGlow160"
        try:
			try:
			    db.img400 = self.driver.find_element_by_css_selector("div.woocommerce-product-gallery.woocommerce-product-gallery--with-images.woocommerce-product-gallery--columns-4.images > figure > div > a > img").get_attribute("srcset").split(",")[0].split()[0]
			except:
			    db.img400 = self.driver.find_element_by_css_selector("div.woocommerce-product-gallery.woocommerce-product-gallery--with-images.woocommerce-product-gallery--columns-4.images > div > figure > div.woocommerce-product-gallery__image.flex-active-slide > a > img").get_attribute("srcset").split(",")[0].split()[0]
        except:
			try:
			    db.img400 = self.driver.find_element_by_css_selector("div.woocommerce-product-gallery.woocommerce-product-gallery--with-images.woocommerce-product-gallery--columns-4.images > div > figure > div.woocommerce-product-gallery__image.flex-active-slide > img").get_attribute("src")
			except:
			    db.img400 = "No/img"
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "WarmGlow800"
        db.img800 = db.img160
        print db
        return db
        
        
    def nextPage(self):
        try:
            self.driver.find_element_by_css_selector("div.mk-pagination-next a").click()
            self.time.sleep(1)
            return True
        except:
            return False



    def get_sitemap(self):
        # fd = requests.get(self.sitemap)
        self.driver.get(self.sitemap)
        self.time.sleep(1)
        # data = xmltodict.parse(fd.content)
        # print data
        # urls = [elem['loc'] for elem in data['urlset']['url']]
        urls = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#sitemap__table > tbody > tr > td > a")]
        print urls

        return urls


    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        self.driver.find_element_by_css_selector("#menu-main-navigation > li.mk-header-search > a").click()
        self.time.sleep(1)
        # while True:
            # try:
        try:
			self.driver.find_element_by_name("s").clear()
        except:
			self.driver.find_element_by_name("hint_q").clear()
        try:
			self.driver.find_element_by_name("s").send_keys(row)
        except:
			self.driver.find_element_by_name("hint_q").send_keys(row)
        try:
			self.driver.find_element_by_name("s").send_keys(Keys.ENTER)
        except:
			self.driver.find_element_by_name("hint_q").send_keys(Keys.ENTER)

        self.time.sleep(1)
        items = []
        result = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("h3.the-title a")]
        result = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("h3.the-title a")]
        print result
        items.extend(result)
        while self.nextPage():
            result = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("h3.the-title a")]
            print result
            items.extend(result)

        return items
