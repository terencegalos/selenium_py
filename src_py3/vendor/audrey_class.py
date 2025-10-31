from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class audrey(domainobject):
    
    def __init__(self,driver,scraper_mode):
        super().__init__(driver)
        self.mode = scraper_mode


    vendor = "Audreys Your Hearts Delight"
    url = "https://audreys.com/account/login/"
    home = "https://www.audreys.com"
    uname = "service@waresitat.com"
    passw = "wolfville"
    delay = 1
    links = []
    
        
    def nextPage(self):
        try:
            if len(self.driver.find_elements(By.CSS_SELECTOR,"a.PageArrow")) == 2:
                self.driver.find_elements(By.CSS_SELECTOR,"a.PageArrow")[0].click()
            else:
                self.driver.find_elements(By.CSS_SELECTOR,"a.PageArrow")[1].click()

            self.time.sleep(1)
            return True
        except:
            print("Page exhausted.")
            return False
        
    def get_links(self):
        items = [l.get_attribute("href") for l in self.driver.find_elements(By.CSS_SELECTOR,"div.thumbnail-grid.clearfix > div > div > div.info > a")]
        print(items)
        return items

    def get_all_items(self):
        cats = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR,"#ctl00_myheader_headerPostLogin > nav > div > ul > li > a")]
        for cat in cats:
            print(cat)
            self.driver.get(cat)
            self.time.sleep(1)

            self.links.extend(self.get_links())
            while self.nextPage():
                self.links.extend(self.get_links())

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_id("ctl00_PageContent_EMail").send_keys(un)
        # self.driver.find_element_by_id("ctl00_PageContent_txtPassword").send_keys(pw)
        # self.driver.find_element_by_id("ctl00_PageContent_txtPassword").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element(By.CSS_SELECTOR,"#wide-col > div > div > ui-view > shopping-container > div > ui-view > shopping-one-up > div > div:nth-child(2) > div.header-text > shopping-one-up-heading > div.oneup-header > h1").text
        db.sku = self.driver.find_element(By.CSS_SELECTOR,"#wide-col > div > div > ui-view > shopping-container > div > ui-view > shopping-one-up > div > div:nth-child(2) > div.header-text > shopping-one-up-heading > div.info > datum:nth-child(1) > div > span:nth-child(2) > span").text
        db.cat = ""#"|".join([c.text for c in self.driver.find_elements(By.CSS_SELECTOR,"a.SectionTitleText")])
        db.desc = ""
        db.stock = ""
        try:
            db.sale = self.driver.find_element(By.CSS_SELECTOR,"span.SalePrice").text
        except:
            db.sale = ""
        db.set = ""
        db.custom = ""
        try:
            db.size = self.driver.find_element(By.CSS_SELECTOR,"#wide-col > div > div > ui-view > shopping-container > div > ui-view > shopping-one-up > div > div:nth-child(2) > div.header-text > shopping-one-up-heading > div.info > datum:nth-child(4) > div > span:nth-child(2) > span").text
        except:
            db.size = ""
        db.seller = ""
        db.min1 = 1
        db.price1 = 99
        # try:
		# 	db.price1 = self.driver.find_element(By.CSS_SELECTOR,"span.RegularPrice").text.encode("utf-8")
        # except:
		# 	db.price1 = self.driver.find_element(By.CSS_SELECTOR,"span.variantprice").text.encode("utf-8")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "Audreys400a"
        db.dir160 = "Audreys160"
        db.img400 = self.driver.find_element(By.CSS_SELECTOR,"#wide-col > div > div > ui-view > shopping-container > div > ui-view > shopping-one-up > div > div:nth-child(2) > div.header-image > product-images > section > div > div.main-images-box.text-center.ng-scope > div > div > a > figure > img").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""#"|".join(self.driver.find_element(By.CSS_SELECTOR,"meta[name='keywords']").text.split())
        db.option = ""
        db.dir800 = "Audreys800"
        db.img800 = db.img160     
        print(db)
        return db
        
        
    def search_item(self,row):
        
        print("\nSearching for item: " + row+"\n")
        while True:
            try:
                self.driver.get(f"https://www.audreys.com/shop/?Search={str(row)}&orderBy=-CreatedOn,Id&context=shop&page=1")
                self.time.sleep(3)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        try:
            items = []
            timeout = 4
            pattern = '//*[@id="wide-col"]/div/div/ui-view/shopping-container/div/ui-view/shopping-multi-view/div/div[2]/div/shopping-multi-view-cards/div/div/div[1]/div/a'
            el = WebDriverWait(self.driver,timeout).until(EC.presence_of_all_elements_located((By.XPATH,pattern)))
            if el:
                item = self.driver.find_element(By.XPATH,pattern).get_attribute("href")
                print(f"link: {item}")
                items.append(item)
            return items
        except TimeoutException:
            print("Item not found.")
            return

