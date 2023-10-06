from helper import table_gateway
from helper import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class pinecreek(domainobject.domainobject):

    vendor = "Pine Creek Four Corners"
    url = "https://www.shoppinecreek.com/customer-login.html"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        try:
            self.driver.find_element_by_css_selector("#JS_PROD > div.content-container > div > div > div > div.row > div.col-sm-7 > div.well.well-prod > a").click()
        except:
            self.driver.get(self.url)
        self.time.sleep(3)
        
        print("Logging in.")
        self.driver.find_element(By.NAME,"Customer_LoginEmail").send_keys(un)
        self.driver.find_element(By.NAME,"Customer_Password").send_keys(pw)
        self.driver.find_element(By.NAME,"Customer_Password").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print("Success.")

    def save_info(self,item=None):
        db = table_gateway.gateway()
        try:
            db.name = self.driver.find_element(By.CSS_SELECTOR,"#JS_PROD > div.content-container > div > div > div > div.row > div.col-sm-7 > h1").text.encode("utf-8")
        except:
            return
        db.sku = self.driver.find_element(By.CSS_SELECTOR,"#JS_PROD > div.content-container > div > div > div > div.row > div.col-sm-7 > div.prod-code > em").text.encode("utf-8")
        try:
            db.cat = self.driver.find_element(By.CSS_SELECTOR,"#main-content div:nth-child(5)").text.encode("utf-8")
        except:
            db.cat = ""
        db.desc = self.driver.find_element(By.CSS_SELECTOR,"#JS_PROD > div.content-container > div > div > div > div.row > div.col-sm-7 > div.prod-desc").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
            db.min1 = self.driver.find_element(By.CSS_SELECTOR,"#JS_PROD > div.content-container > div > div > div > div.row > div.col-sm-7 > form > div.well.well-prod > div > div.col-sm-3.col-xs-4 > select > option:nth-child(1)").get_attribute("value")
        except:
            db.min1 = self.driver.find_element(By.NAME,"Quantity").get_attribute("value")
        try:
            db.price1 = self.driver.find_element(By.CSS_SELECTOR,"#price-value").text.encode("utf-8")
        except:
            db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "PineCreek400"
        db.dir160 = "PineCreek160"
        db.img400 = self.driver.find_element(By.CSS_SELECTOR,"#main_image").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "PineCreek800"
        db.img800 = db.img160
        print(db)
        return db

    def get_info(self,item=None):
        while True:
            try:
                db = self.save_info()
                return db
                break
            except:
                self.init_login(self.uname,self.passw)
                db = self.save_info()
                return db
                break
        
        
    def search_item(self,row):
        
        print("\nSearching for item: " + row+"\n")
        # if len(row.split(",")[1].strip()) > 1:
        while True:
            try:
                self.driver.find_element(By.NAME,"Search").clear()
                self.driver.find_element(By.NAME,"Search").send_keys(row)
                self.driver.find_element(By.NAME,"Search").send_keys(self.Keys.ENTER)
                self.time.sleep(2)
                break
            except Exception as e:
                print("Search fail:")
                print(e)
                self.driver.refresh()
                self.time.sleep(1)
                continue
        try:
            items = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"#JS_SRCH > div.content-container > div > div > div > div.row.row-masonry > div.ctgy-item > a")]
            return items
        except:
            return None
            

