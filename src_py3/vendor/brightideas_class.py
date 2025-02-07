from helper.table_gateway import gateway
from  helper.domainobject import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class brightideas(domainobject):

    vendor = "Bright Ideas"
    url = "https://brightideasllc.com"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    lastStop = "https://www.brightideasllc.com/product/sm-standing-plush-grey-santa-gnome"
    flag = False
    
                
    def nextPage(self):
        try:
            self.driver.find_element(By.LINK_TEXT,"Next").click()
            self.time.sleep(2)
            return True
        except:
            print("Page exhausted.")
            return False

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element(By.NAME,"username").send_keys(un)
        # self.driver.find_element(By.NAME,"passwd").send_keys(pw)
        # self.driver.find_element(By.NAME,"passwd").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(5) > div > div > div > form > div > h3").text
        db.sku = self.driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(5) > div > div > div > form > div > p:nth-child(3)").text
        db.cat = ""
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
        db.dir400 = "brightideas400"
        db.dir160 = "brightideas160"
        try:
            db.img400 = self.driver.find_element(By.CSS_SELECTOR,"#pic_1 > a").get_attribute("href")
        except:
            db.img400 = "NA"
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "brightideas800"
        db.img800 = db.img160
        print(db)
        return db
        
        
    def search_item(self,row):
        print("\nSearching for item: " + row+"\n")
		# while True:
        try:
            search = self.driver.find_element(By.NAME,"q")
            search.clear()
            search.send_keys(str(row))
            search.send_keys(Keys.ENTER)
            self.time.sleep(2)
        except:
            search = self.driver.find_element(By.NAME,"productName")
            search.clear()
            search.send_keys(str(row))
            search.send_keys(Keys.ENTER)
            self.time.sleep(1)

            # 	break
            # except:
            # 	self.driver.refresh()
            # 	self.time.sleep(1)
            # 	continue
        items = []
        item = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR,"#listedproduct > div > form > div > h5 > a")]
        print(item)
        items.extend(item)
        while self.nextPage():
            item = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR,"#listedproduct > div > form > div > h5 > a")]
            print(item)
            items.extend(item)


        return items