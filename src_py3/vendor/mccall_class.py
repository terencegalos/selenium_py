from helper.table_gateway import gateway
from helper.domainobject import domainobject
import json

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import xml.etree.ElementTree as tree
import requests,xmltodict

class mccall(domainobject):

    def __init__(self,driver,mode=None):
        self.driver = driver
        self.mode = mode
    
    vendor = "McCall's Candles"
    # sitemap = "http://mccallscandles.com/sitemap.xml"
    # sitemap = "https://mccallscandles.com/sitemap_products_1.xml?from=5854385340579&to=5868063064227"
    sitemap = "https://mccallscandles.com/sitemap_products_1.xml?from=5854385340579&to=8387160211699"
    url = "https://www.carsonhomeaccents.com/security_logon.asp?autopage=%2Fdefault%2Easp"
    home = "https://mccallscandles.com/"
    uname = "rstuart"
    passw = "Wolfville4"
    delay = 1
    links = []
    flag = False
    lastStop = ""

    def get_all_items(self):
        self.read_sitemap()
    
    def read_sitemap(self):
        xmlfile = requests.get(self.sitemap)
        self.time.sleep(1)
        data = xmltodict.parse(xmlfile.content)
        print(data)
        self.links.extend([link['loc'] for link in data['urlset']['url']])
        
    def init_login(self,un,pw):
        self.driver.get(self.home)
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#sw_dropdown_778 > a")).perform()
        # self.time.sleep(1)
        # print "Logging in..."
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "logonUsername"))).send_keys(un)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "logonPassword"))).send_keys(pw)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "logonPassword"))).send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element(By.CSS_SELECTOR,"#ProductSection-product-template > div > div:nth-child(2) > div.product-single__meta > h1").text
        except:
            return None
        # try:
			# db.sku = self.driver.find_element(By.CSS_SELECTOR,"div[itemprop=sku]").text.encode("utf-8")
        jsonText = self.driver.find_element(By.CSS_SELECTOR,"#ProductJson-product-template").get_attribute("innerHTML")
        print("\n"+jsonText+"\n")
        pd = json.loads(jsonText)
        print
        print(pd['variants'][0]['sku'])
        print
        db.sku = pd['variants'][0]['sku']
        # except:
			# db.sku = item
        db.cat = ""#self.driver.find_element(By.CSS_SELECTOR,"#product-attribute-specs-table > tbody > tr:nth-child(6) > td").text.encode("utf-8")
        db.desc = self.driver.find_element(By.CSS_SELECTOR,"div.product-single__description.rte").text
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""#self.driver.find_element(By.CSS_SELECTOR,"#product-attribute-specs-table > tbody > tr:nth-child(5) > td").text.encode("utf-8")
        db.seller = ""
        db.min1 = 1
        db.price1 = self.driver.find_element(By.CSS_SELECTOR,"#ProductSection-product-template > div > div:nth-child(2) > div.product-single__meta > div > dl > div.price__pricing-group > div.price__regular > dd > span").text
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "mccandles400"
        db.dir160 = "mccandles160"
        self.time.sleep(1)
        # db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#maincontent > div.alocolumns > div > div.product-view > div > div > div.product.media.product-img-box.clearfix.col-md-5.col-sm-5.col-xs-12 > div > div.fotorama-item.fotorama.fotorama1532553261938 > div.fotorama__wrap.fotorama__wrap--css3.fotorama__wrap--slide.fotorama__wrap--toggle-arrows.fotorama__wrap--css2.fotorama__wrap--no-shadows.fotorama__wrap--no-controls > div.fotorama__stage > div.fotorama__stage__shaft > div > img.fotorama__img"))).get_attribute("src")
        # while True:
        try:
            db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.zoomImg"))).get_attribute("src")
        except:
            db.img400 = "No image."

        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "mccandles800"
        db.img800 = db.img160
        print(db)
        return db
        
        
    def search_item(self,row):
        
        print("\nSearching for item: " + row+"\n")
        # while True:
            # try:

        ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#shopify-section-header > div:nth-child(3) > header > div > div.grid__item.medium-up--one-fifth.text-right.site-header__icons.site-header__icons--plus > div > button.btn--link.site-header__icon.site-header__search-toggle.js-drawer-open-top")).perform()
        self.driver.find_element(By.CSS_SELECTOR,"#shopify-section-header > div:nth-child(3) > header > div > div.grid__item.medium-up--one-fifth.text-right.site-header__icons.site-header__icons--plus > div > button.btn--link.site-header__icon.site-header__search-toggle.js-drawer-open-top").click()
        self.time.sleep(1)
        self.driver.find_element(By.NAME,"q").clear()
        self.driver.find_element(By.NAME,"q").send_keys(row)
        self.driver.find_element(By.NAME,"q").send_keys(Keys.ENTER)
        # self.driver.get("https://mccallscandles.com/catalogsearch/result/?q="+row)
        self.time.sleep(1)
            #     break
            # except:
            #     self.driver.refresh()
            #     continue
        try:
            item = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"#MainContent > ul > li > div > a")]
            return item
        except:
            return None
