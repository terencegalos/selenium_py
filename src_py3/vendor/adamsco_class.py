from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class adamsco(domainobject):

    vendor = "Adams and Company"
    url = "https://www.adamsandco.net/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR,"#account-links__button").click()
        self.time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR,"#account-links__content > div:nth-child(7) > a > div:nth-child(2)").click()
        self.time.sleep(1)
        print("Logging in.")
        self.driver.find_element(By.NAME,"email").send_keys(un)
        self.driver.find_element(By.NAME,"password").send_keys(pw)
        self.driver.find_element(By.NAME,"password").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print("Success.")

    def get_info(self,item=None):
        
        db = gateway()
        db.name = self.driver.find_element(By.CSS_SELECTOR,"body > div.product.margin--percent > div > div.flex-row.product-container > div.summary.summary-margin.flex-column.flex--justify-start > span.margin--viewport--small > h1").text.encode("utf-8").strip()
        try:
            # db.sku = self.driver.find_element(By.CSS_SELECTOR,"span[itemprop='sku']").text.encode("utf-8").strip()
            db.sku = self.driver.find_element(By.CSS_SELECTOR,"body > div.product.margin--percent > div > div.flex-row.product-container > div.summary.summary-margin.flex-column.flex--justify-start > span.margin--viewport--small > h1").text.split()[0]
        except:
            db.sku = self.driver.find_element(By.CSS_SELECTOR,"span[itemprop='mpn']").text.encode("utf-8")
        db.cat = ""
        db.desc = ""#self.driver.find_element(By.CSS_SELECTOR,"p[itemprop='description']").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""#self.driver.find_element(By.CSS_SELECTOR,"body > div.product.container > div > div.description.col-tablet-7 > ul > li:nth-child(2)").text.encode("utf-8")
        db.seller = ""
        db.min1 = self.driver.find_element(By.CSS_SELECTOR,"body > div.product.margin--percent > div > div.flex-row.product-container > div.summary.summary-margin.flex-column.flex--justify-start > div.margin--viewport--small.flex-row.flex--wrap.flex--align-center.flex--justify-start > div.actions > form > div > input").get_attribute("value").encode("utf-8").strip()
        db.price1 = self.driver.find_element(By.CSS_SELECTOR,"body > div.product.margin--percent > div > div.flex-row.product-container > div.summary.summary-margin.flex-column.flex--justify-start > span.pricing > div.item_price.margin--viewport--small > div > span > span.price").text.encode("utf-8").strip()
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "Adams400"
        db.dir160 = "Adams160"
        db.img400 = self.driver.find_element(By.CSS_SELECTOR,"#main_image > a > span > img").get_attribute("src").encode("utf-8").strip()
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""#self.driver.find_element(By.CSS_SELECTOR,"body > div.product.container > div > div.description > p").text.encode("utf-8")
        db.option = ""
        db.dir800 = "Adams800"
        db.img800 = db.img160
        print(db)
        return db
        
        
    def search_item(self,row):
        
        print("\nSearching for item: " + str(row)+"\n")
        # while True:
        #     try:
        self.driver.find_element(By.NAME,"query").clear()
        self.driver.find_element(By.NAME,"query").send_keys(row)
        self.driver.find_element(By.NAME,"query").send_keys(self.Keys.ENTER)
        self.time.sleep(1)
            #     break
            # except:
            #     self.driver.refresh()
            #     self.time.sleep(1)
            #     continue

        try:
            items = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"body > div.category.container > div > div.products.list.col-tablet-9 > div.product.container-fluid > div > div.summary.col-tablet-8.col-phone-7 > div.title > a")]
            print(items)
            return items
        except:
            print("Getting info directly.")
            return None

