from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests, xmltodict

class hannas(domainobject):

    vendor = "Hanna's Handiworks"
    products = "https://www.hannashandiworks.com/products.html"
    url = "http://www.hannashandiworks.com/"
    home = "http://www.hannashandiworks.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    lastStop = "https://www.hannashandiworks.com/products.html?p=58"
    delay = 1
    flag = 0
    
    links = [] #for scraper; links to all items
    
        
    def nextPage(self):
        try:
            # self.driver.find_elements(By.CSS_SELECTOR,"a[title=Next]")[-1:].click()
            # self.driver_execute_script("window.scrollTo(0,document.body.scrollHeight)")
            self.time.sleep(5)
            self.driver.find_element(By.CSS_SELECTOR,"body").send_keys(Keys.END)
            self.time.sleep(5)
            self.driver.find_element(By.CSS_SELECTOR,"#layer-product-list > div:nth-child(4) > div.pages > ul > li.item.pages-item-next > a").click()
            return True
        except:
            print("Page exhausted.")
            return False

    def get_all_items(self):
        # print link
        xmlfile = requests.get("https://www.hannashandiworks.com/sitemap.xml")
        self.time.sleep(1)
        data = xmltodict.parse(xmlfile.content)
        print(data)

        self.links.extend([d['loc'] for d in data['urlset']['url'] if d['loc'] not in self.links])

    def init_login(self,un,pw):
        self.driver.get("https://www.hannashandiworks.com/customer/account/login/")
        self.time.sleep(1)
        
        print("Logging in.")
        
        # self.driver.find_element(By.CSS_SELECTOR,"#store\.menu > nav > ul > li:nth-child(7) > a").click()
        self.time.sleep(1)
        self.driver.find_element(By.NAME,"login[username]").send_keys(un)
        self.driver.find_element(By.NAME,"login[password]").send_keys(pw)
        self.driver.find_element(By.NAME,"login[password]").send_keys(Keys.ENTER)
        # self.driver.execute_script('document.querySelector("input[type=password]").setAttribute("value",arguments[0])',pw)
        # self.driver.execute_script('document.forms[0].submit();')
        self.time.sleep(1)
        print("Success.")

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > div.page-title-wrapper.product > h1 > span").text
        except:
            # self.time.sleep(3)
            # self.driver.refresh()
            # self.time.sleep(1)
            # db.name = self.driver.find_element(By.CSS_SELECTOR,"#product_addtocart_form > div.product-shop > div.product-name > span.h1").text
            return None

        db.sku = WebDriverWait(self.driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > div.product-info-price > div.product-info-stock-sku > div.product.attribute.sku > div"))).text
        db.cat = ""
        try:
            db.desc = self.driver.find_element(By.CSS_SELECTOR,"#description > div").text.encode("latin-1")
        except:
            db.desc = ""
        try:
            db.stock = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > div.product-info-price > div.product-info-stock-sku > div.stock.available > span:nth-child(2)").text
        except:
            db.stock = ""
        try:
            db.sale = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > div.product-info-price > div.price-box.price-final_price > span.special-price > span > span.price-wrapper > span").text
        except:
            db.sale = ""
        db.set = ""
        db.custom = ""
        try:
            db.size = self.driver.find_element(By.CSS_SELECTOR,"#description > div").text
        except:
            db.size = ""
        db.seller = ""
        try:
            db.min1 = self.driver.find_element(By.CSS_SELECTOR,"#qty").get_attribute("value")
        except:
            db.min1 = "NA"
        try:
            db.price1 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > div.product-info-price > div.price-box.price-final_price > span.old-price > span > span.price-wrapper > span").text
        except:
            db.price1 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > div.product-info-price > div.price-box.price-final_price > span > span > span").text
        try:
            db.min2 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > ul > li:nth-child(1)").text.split()[1]
        except:
            db.min2 = ""
        try:
            db.price2 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > ul > li:nth-child(1)").text.split()[3]
        except:
            db.price2 = ""
        try:
            db.min3 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > ul > li:nth-child(2)").text.split()[1]
        except:
            db.min3 = ""
        try:
            db.price3 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > ul > li:nth-child(2)").text.split()[3]
        except:
            db.price3 = ""
            
        db.multi = db.min1
        db.dir400 = "Hannas400"
        db.dir160 = "Hannas160"
        try:
            db.img400 = self.driver.find_element(By.CSS_SELECTOR,"img.fotorama__img").get_attribute("src")
        except:
            try:
                db.img400 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product.media > div.gallery-placeholder._block-content-loading > img").get_attribute("src")
            except:
                return None

        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""#self.driver.find_element(By.CSS_SELECTOR,"#product-attribute-specs-table > tbody > tr > td").text
        db.dir800 = "Hannas800"
        db.img800 = db.img160     
        db.img800 = db.img160     
        print(db)
        return db
        
        
    def search_item(self,row):
        print("\nSearching for item: " + row+"\n")
        # self.driver.get("https://www.hannashandiworks.com/products/fall.html")
        # self.time.sleep(1)
        self.links = []
        while True:
            try:
                self.driver.find_element(By.NAME,"q").clear()
                self.driver.find_element(By.NAME,"q").send_keys(str(row))
                self.driver.find_element(By.NAME,"q").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.get(self.products)
                self.time.sleep(10)
                continue

        # try:
        # self.driver.get(self.lastStop)
        # self.time.sleep(1)
        item = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"#layer-product-list > div > div.products.wrapper.grid.columns4.products-grid > ol > li > div > div.product.details.product-item-details > strong > a") if i.get_attribute("href") not in self.links]
        # item = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"#layer-product-list > div.products.wrapper.grid.columns4.products-grid > ol > li > div > div.product.details.product-item-details > strong > a") if i.get_attribute("href") not in self.links]
        print(item)
        self.links.extend(item)
        # while self.nextPage():
        #     try:
        #         item = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"#layer-product-list > div.products.wrapper.grid.columns4.products-grid > ol > li > div > div.product.details.product-item-details > strong > a") if i.get_attribute("href") not in self.links]
        #     except:
        #         self.driver.refresh()
        #         self.time.sleep(1)
        #         item = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"#layer-product-list > div.products.wrapper.grid.columns4.products-grid > ol > li > div > div.product.details.product-item-details > strong > a") if i.get_attribute("href") not in self.links]
        #     print item
        #     self.links.extend(item)
            
        return self.links

        # except:
        #     return None

