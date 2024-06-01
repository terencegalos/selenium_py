import json
from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class homespice(domainobject):

    vendor = "Homespice D\xe9cor"
    url = "https://www.homespice.com/"
    home = "https://www.homespice.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    test = True
    item = 591142
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        # self.driver.find_element(By.CSS_SELECTOR,"#site > header > div > div > div.navigation > div > nav > ul:nth-child(2) > li:nth-child(3) > a").click()
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element(By.CSS_SELECTOR,"body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > modal > div.modal-body > modal-body > div.row.m-a-3 > div > login-fieldset > div:nth-child(1) > div > div > div:nth-child(1) > div > input").send_keys(un)
        # self.driver.find_element(By.CSS_SELECTOR,"body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > modal > div.modal-body > modal-body > div.row.m-a-3 > div > login-fieldset > div:nth-child(2) > div > div > div:nth-child(1) > div > input").send_keys(pw)
        # self.driver.find_element(By.CSS_SELECTOR,"body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > modal > div.modal-body > modal-body > div.row.m-a-3 > div > login-fieldset > div:nth-child(2) > div > div > div:nth-child(1) > div > input").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element(By.CSS_SELECTOR,"div.product__head > h1").text.encode("utf-8")
        # db.sku = self.driver.find_element(By.CSS_SELECTOR,"body > script:nth-child(24)").execute_script("document.onload(function() {return google_tag_params.ecomm_prodid;});")
        db.sku = item
        # sk= self.driver.find_element(By.CSS_SELECTOR,"body > div.wrapper.ps-static.en-lang-class > div.page > div.main-container.col1-layout > div > div > div > div > div.col-main > div.padding-s > script:nth-child(2)").get_attribute("innerHTML")
        # sc =self.driver.execute_script('var sc = document.querySelectorAll("body > div.wrapper.ps-static.en-lang-class > div.page > div.main-container.col1-layout > div > div > div > div > div.col-main > div.padding-s > script:nth-child(2)")[0].innerHTML; return sc;')
        # print sc
        # sk = sc.strip()
        # js = json.loads("'"+sk+"'")
        # print sk
		
        # self.time.sleep(30)
        # print sc['offers']
        # print json.load("'"+sk+"'")
        db.cat = ""
        db.desc = self.driver.find_element(By.CSS_SELECTOR,"div.product__wrap > div.product__about > dl > dd").text.encode("utf-8")
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
        db.dir400 = "Homespice400"
        db.dir160 = "Homespice160"
        try:
            db.img400 = self.driver.find_element(By.CSS_SELECTOR,"#zoom1").get_attribute("href")
        except Exception as e:
            print(e)
            self.time.sleep(3)
            return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Homespice800"
        db.img800 = db.img160
        print(db)
        return db
        
        
    def search_item(self,row):
        print("\nSearching for item: " + row+"\n")
        while True:
            try:
                # self.driver.find_element(By.CSS_SELECTOR,"#menu > li.search").click()
                # self.time.sleep(0.5)
                # self.driver.find_element(By.NAME,"q").clear()
                # self.driver.find_element(By.NAME,"q").send_keys(str(row))
                # self.driver.find_element(By.NAME,"q").send_keys(Keys.ENTER)
                self.driver.get(f"https://homespice.com/search/{str(row)}")
                self.time.sleep(self.delay)
                break
            except:
                self.driver.get(self.url)
                self.time.sleep(self.delay)
                continue

        try:
            item = self.driver.find_element(By.CSS_SELECTOR,"#kuLandingProductsListUl > li > div.klevuImgWrap > a").get_attribute("href")
            print(item)
            return [item]
        except:
            return None

