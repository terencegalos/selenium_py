from table_gateway import gateway
import domainobject
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re

class whdsale(domainobject.domainobject):

    vendor = "Wholesale Home Decor Closeouts"
    url = "https://whdfloral.com/customer/account/login/"
    home = "http://whdfloral.com/"
    search = "https://whdfloral.com/catalogsearch/result/?q="
    uname = "rick@waresitat.com"
    passw = "Wolfville4"
    delay = 1
    links = []
    modeFlag = 1
        
    def nextPage(self):
        
        try:
            self.driver.find_elements_by_css_selector("ul > li.item.pages-item-next > a")[-1].click()
            self.time.sleep(10) # 3 secs to load
            return True

        except:
            print "Page exhausted."
            return False

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(10)
        # print self.driver.find_element_by_css_selector("#login-form").get_attribute("innerHTML")
        
        print "Logging in."
        self.driver.find_element_by_css_selector("#login-form #email").send_keys(self.uname)
        self.driver.find_element_by_css_selector("#login-form #pass").send_keys(self.passw)
        self.time.sleep(5)
        self.driver.find_element_by_css_selector("#login-form #pass").send_keys(Keys.ENTER)
        # self.driver.find_element_by_css_selector("#send2 > span.mdl-button__ripple-container").click()
        print "Success."
        self.time.sleep(5)

    def get_info(self,item=None):
        
        db = gateway()
        self.time.sleep(1)

        try:
            db.name = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.page-title-wrapper.product > h1 > span"))).text.encode("utf-8")
        except:
            self.time.sleep(1)
            self.driver.refresh()
            self.time.sleep(1)
            db.name = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.page-title-wrapper.product > h1 > span"))).text.encode("utf-8")
            
        db.sku = self.driver.find_element_by_css_selector("div.product.attribute.sku > div").text
        db.cat = ""
        try:
            db.desc = self.driver.find_element_by_css_selector("#description > div > div").text.encode("utf-8")
        except:
            db.desc = ""

        try:
            db.stock = self.driver.find_element_by_css_selector("#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-primary-column.product-shop.grid12-5.product-info-main > div.stock.available > span").text
        except:
            try:
                db.stock = self.driver.find_element_by_css_selector("#product_addtocart_form > div > div.product-right.col-sm-12 > div.product-info-main-inner > div.product-info-price > div.product-info-stock-sku > div.stock").text
            except:
                db.stock = ""

        # db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""

        try:
            db.min1 = self.driver.find_element_by_css_selector("#qty").get_attribute("value")
        except:
            db.min1 = 1

        try:
            db.price1 = self.driver.find_element_by_css_selector("#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-primary-column.product-shop.grid12-5.product-info-main > div.product-info-main > div.product-info-price > div.price-box.price-final_price > span.old-price > span > span.price-wrapper > span").text.encode("utf-8").strip("$")
            db.sale = self.driver.find_element_by_css_selector("#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-primary-column.product-shop.grid12-5.product-info-main > div.product-info-main > div.product-info-price > div.price-box.price-final_price > span.special-price > span > span.price-wrapper").text.encode("utf-8").strip("$")
        except:
            db.price1 = self.driver.find_element_by_css_selector("#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-primary-column.product-shop.grid12-5.product-info-main > div.product-info-main > div.product-info-price > div.price-box.price-final_price > span > span > span").text.encode("utf-8").strip("$")

        try:
            db.min2 = self.driver.find_element_by_css_selector("#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-primary-column.product-shop.grid12-5.product-info-main > div.product-info-main > ul > li:nth-child(1)").text.split()[1]
            db.price2 = self.driver.find_element_by_css_selector("#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-primary-column.product-shop.grid12-5.product-info-main > div.product-info-main > ul > li:nth-child(1)").text.split()[3].strip("$")
        except:
            db.min2 = ""
            db.price2 = ""

        try:
            db.min3 = self.driver.find_element_by_css_selector("#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-primary-column.product-shop.grid12-5.product-info-main > div.product-info-main > ul > li:nth-child(2)").text.split()[1]
            db.price3 = self.driver.find_element_by_css_selector("#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-primary-column.product-shop.grid12-5.product-info-main > div.product-info-main > ul > li:nth-child(2)").text.split()[3].strip("$")
        except:
            db.min3 = ""
            db.price3 = ""

        db.multi = db.min1
        db.dir400 = "Harv400"
        # db.dir160 = "Harv160"
        # self.driver.execute_script("""
        # var jq = document.createElement('script');
        # jq.type = 'text/javascript';
        # jq.src = 'https://code.jquery.com/jquery-3.4.1.min.js';
        # jq.integrity = 'sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=';
        # jq.crossorigin = 'anonymous';
        # document.getElementsByTagName('head')[0].append(jq); """)

        # self.driver.execute_script('''
        #         if(document.readyState="Loading"){
        #             document.addEventListener("DOMContentLoaded",function(){
        #                 var img=document.querySelector("#product_addtocart_form > div > div.product-left.col-sm-12"); 
        #                 img.parentNode.removeChild(img);
        #             });
        #         }
        # ''')
        
        # WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#product_addtocart_form > div > div.product-left.col-sm-12"))) #detect items for 3 seconds
        # WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-img-column"))) #detect items for 3 seconds
        # self.driver.execute_script('window.stop(); var img=document.querySelector("#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-img-column"); img.parentNode.innerHTML = "<script type=text/javascript></script>";')
        # db.img400 = "http://imagecat/imagename.jpg"

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.fotorama__stage__shaft > div > img"))).get_attribute("src")
            db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.fotorama__stage__shaft > div > img"))).get_attribute("src")
        except:
            self.driver.refresh()
            self.time.sleep(1)
            try:
                db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.fotorama__stage__shaft > div > img"))).get_attribute("src")
            except:
                db.img400 = "http://imagecat/imagename.jpg"

        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Harv800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        self.links = []

        print "\nSearching for item: " + row+"\n"
        print self.search+row

        self.driver.get(self.search+row)
        self.time.sleep(1)

        items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("div.product.details.product-item-details > strong > a") if i.get_attribute("href") not in self.links]
        print items
        # self.links.extend(items) 
            
        return self.links

        # self.driver.get(r'https://whdfloral.com/catalogsearch/result/?q=" "')
        # https://whdfloral.com/catalogsearch/result/?q=""