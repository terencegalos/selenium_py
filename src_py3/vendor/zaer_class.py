import json
from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class zaer(domainobject):

    vendor = "Zaer Ltd. International"
    url = "https://www.zaerltd.com/"
    login = "https://www.zaerltd.com/"
    home = "https://www.zaerltd.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville4"
    delay = 1
    links = []

    def __init__(self,driver,scraping_mode):
        self.driver = driver
        self.mode = scraping_mode
    
        
    def init_login(self,un,pw):
        self.driver.get(self.login)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element(By.NAME,"customer[email]").send_keys(un)
        # self.driver.find_element(By.NAME,"customer[password]").send_keys(pw)
        # self.driver.find_element(By.NAME,"customer[password]").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."
        
	
    def get_info(self,item=None):
        db = gateway()
        print("Getting item info.")
        db.name = self.driver.find_element(By.CSS_SELECTOR,"#commerce > div > div.COMProdRightContainer.col-12.col-md-6 > div.COMProdHeader > h1").text
        db.sku =  self.driver.find_element(By.CSS_SELECTOR,"#ProductItemCode").text
        self.time.sleep(1)
        db.cat = "|".join([a.text for a in self.driver.find_elements(By.CSS_SELECTOR,"#catprodBreadcrumb > ol > li.breadcrumb-item")])
        try:
            db.desc = self.driver.find_element(By.CSS_SELECTOR,"#COMProdDesc").text
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
        db.dir400 = "Zaer400"
        db.dir160 = "Zaer160"
        db.img400 = self.driver.find_element(By.CSS_SELECTOR,"#COMProdImage").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Zaer800"
        db.img800 = db.img160
        print(db.retrieve())
        return db
        
        
    def search_item(self,row):
        print("\nSearching for item: " + row+"\n")
        while True:
            try:
                self.driver.find_element(By.NAME,"SearchText").click()
                self.time.sleep(0.5)
                self.driver.find_element(By.NAME,"SearchText").clear()
                self.driver.find_element(By.NAME,"SearchText").send_keys(str(row))
                self.driver.find_element(By.NAME,"SearchText").send_keys(Keys.ENTER)
                self.time.sleep(self.delay)
                break
            except:
                self.driver.get(self.url)
                self.time.sleep(self.delay)
                continue

        try:
            item = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"#productsResult > div > div.prodDetails > div.prodName > a")]
            print(item)
            return item
        except:
            return None

