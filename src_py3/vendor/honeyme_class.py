from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class honeyme(domainobject):

    vendor = "Honey & Me"
    url = "http://www.honeyandme.com/shop/"
    home = "http://www.honeyandme.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville4"
    delay = 1
    lastStop = "https://honeyandme.com/e170139-small-metal-wide-star-6-pc-set/"
    flag = False
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR,"body > header > div.upper-header > a.upper-header-item.account-wrapper").click()
        self.time.sleep(2)
        
        print("Logging in.")
        self.driver.find_element(By.NAME,"login_email").send_keys(un)
        self.driver.find_element(By.NAME,"login_pass").send_keys(pw)
        self.driver.find_element(By.NAME,"login_pass").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print("Success.")

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element(By.CSS_SELECTOR,"#form-add-to-cart > div > div > h1").text.encode("utf-8")
        except:
            try:
                self.driver.refresh()
                self.time.sleep(1)
                db.name = self.driver.find_element(By.CSS_SELECTOR,"#form-add-to-cart > div > div > h1").text.encode("utf-8")
            except:
                return None

        db.sku = db.name.split()[0]
        db.cat = "|".join([i.text.encode("utf-8") for i in self.driver.find_elements(By.CSS_SELECTOR,"body > header > div.lower-header > div > section > span > span.breadcrumb > span.breadcrumb > a")])
        db.desc = ""
        try:
            db.stock = self.driver.find_element(By.CSS_SELECTOR,"#additional-info > div:nth-child(2) > span.product-additional-info-item-value").text
        except:
            db.stock = ""
		
        try:
            db.sale = self.driver.find_element(By.CSS_SELECTOR,"#form-add-to-cart > div > div > div.product-price > div > div.product-price-saved-num > span:nth-child(2)").text.replace("$","")
        except:
            db.sale = ""
			
        db.set = ""
        db.custom = ""
		
        try:
            db.size = self.driver.find_element(By.CSS_SELECTOR,"#additional-info > div:nth-child(4)").text.encode("utf-8")
        except:
            db.size = ""
			
        db.seller = ""
		
        try:
            db.min1 = self.driver.find_element(By.CSS_SELECTOR,"#form-add-to-cart > div > div > div.add-to-cart-quantity-container > div > label > span.form-field-quantity-control > span > input").get_attribute("value")
        except:
            db.min1 = "N/A"
			
        try:
            db.price1 = self.driver.find_element(By.CSS_SELECTOR,"#form-add-to-cart > div > div > div.product-price > div > div > span").text.encode("utf-8").replace("$","")
        except:
            return None
        # print db.price1
		
        try:
            db.min2 = self.driver.find_element(By.CSS_SELECTOR,"#form-add-to-cart > div > div > div.bulk-pricing-block > ul > li").text.split()[1]
        except:
            db.min2 = ""
			
        db.price2 = float(db.price1) * .9 if db.min2 != "" else db.min2
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "Honeyme400"
        db.dir160 = "Honeyme160"
		
        try:
            db.img400 = self.driver.find_element(By.CSS_SELECTOR,"#product-images > div > div > div > a > img").get_attribute("src").split("?")[0]
        except:
            return
			
        db.img160 = db.img400.split("/")[-1:][0]    
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Honeyme800"
        db.img800 = db.img160     
        print(db)
        # self.time.sleep(5)
        return db
        
        
    def search_item(self,row):
        self.driver.find_element(By.CSS_SELECTOR,"body > header > div.upper-header > button.upper-header-item.search-wrapper").click()
        self.driver.find_element(By.CSS_SELECTOR,"button.upper-header-item:nth-child(3)").click()
        print("\nSearching for item: " + row+"\n")
        while True:
            try:
                # self.driver.find_element(By.NAME,"search_query").clear()
                self.driver.find_element(By.NAME,"search_query").send_keys(str(row))
                self.driver.find_element(By.NAME,"search_query").send_keys(self.Keys.ENTER)
                self.time.sleep(2)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        try:
            item = self.driver.find_element(By.CSS_SELECTOR,"body > main > section.catalog-wrapper.tab-search-results.tab-product-results.tab-selected > main > div > div.product-listing > article:nth-child(1) > div.product-item-info > h3 > a").get_attribute("href")
            print(item)
            return [item]
        except:
            return None

