from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class homart(domainobject.domainobject):

    vendor = "HomArt"
    url = "https://homart.com/"
    home = "https://homart.com/"
    uname = "Rick.waresitat@gmail.com"
    passw = "wolfville"
    delay = 1
    links = []
    
        
    def nextPage(self):
        try:
            if len(self.driver.find_elements_by_css_selector("a.PageArrow")) == 2:
                self.driver.find_elements_by_css_selector("a.PageArrow")[0].click()
            else:
                self.driver.find_elements_by_css_selector("a.PageArrow")[1].click()

            self.time.sleep(1)
            return True
        except:
            print "Page exhausted."
            return False
        
    def get_links(self):
        items = [l.get_attribute("href") for l in self.driver.find_elements_by_css_selector("div.thumbnail-grid.clearfix > div > div > div.info > a")]
        print items
        return items

    def get_all_items(self):
        cats = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#ctl00_myheader_headerPostLogin > nav > div > ul > li > a")]
        for cat in cats:
            print cat
            self.driver.get(cat)
            self.time.sleep(1)

            self.links.extend(self.get_links())
            while self.nextPage():
                self.links.extend(self.get_links())

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_css_selector(".cd-signin").click()
        self.time.sleep(1)
        self.driver.find_element_by_id("username").send_keys(un)
        self.driver.find_element_by_id("password").send_keys(pw)
        self.driver.find_element_by_id("password").send_keys(Keys.ENTER)
        self.time.sleep(10)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        # db.name = self.driver.find_element_by_css_selector(".product-item-item-detail").text.encode("utf-8")
        db.name = WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".product-item-item-detail"))).text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector(".productDetail-item-pnumber > span:nth-child(2)").text.encode("utf-8")
        db.cat = ""
        db.desc = self.driver.find_element_by_css_selector("div.product-item-long-description:nth-child(6)").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element_by_css_selector("table.product-item-specs:nth-child(8) > tbody:nth-child(1)").text.encode("utf-8")
        db.seller = ""
        db.min1 = self.driver.find_element_by_css_selector("table.product-item-prices:nth-child(12) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3)").text.encode("utf-8").split()[1]
        db.price1 = self.driver.find_element_by_css_selector("table.product-item-prices:nth-child(12) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1)").text.encode("utf-8").split("/")[0]
        try:
            db.min2 = self.driver.find_element_by_css_selector("table.product-item-prices:nth-child(12) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3)").text.encode("utf-8").split()[1]
            db.price2 = self.driver.find_element_by_css_selector("table.product-item-prices:nth-child(12) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)").text.encode("utf-8").split("/")[0]
        except:
            db.min2 = ""
            db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = self.driver.find_element_by_css_selector("table.product-item-prices:nth-child(12) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3)").text.encode("utf-8").split()[1]
        db.dir400 = "homart400"
        db.dir160 = "homart160"
        # db.img400 = self.driver.find_element_by_css_selector("div.collection-items-container:nth-child(3) > div:nth-child(1) > img:nth-child(1)").get_attribute("src").replace("https://homart.com/images/products/list/desktop/","https://homart.com/images/products/ZOOM/desktop/")
        # db.img400 = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.collection-items-container:nth-child(3) > div:nth-child(1) > img:nth-child(1)"))).get_attribute("src").replace("https://homart.com/images/products/list/desktop/","https://homart.com/images/products/ZOOM/desktop/")
        db.img400 = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-detail-main-image"))).get_attribute("data-zoom-image")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "homart800"
        db.img800 = db.img160     
        print db
        # self.time.sleep(5)
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_css_selector("#algolia-searchString").clear()
                self.driver.find_element_by_css_selector("#algolia-searchString").send_keys(str(row))
                self.time.sleep(1)
                self.driver.find_element_by_css_selector("#algolia-searchString").send_keys(self.Keys.ENTER)
                self.time.sleep(5)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        # self.driver.find_element_by_css_selector("body > div:nth-child(11) > div > div > div.col-lg-10.col-sm-9.col-xs-12 > div:nth-child(2) > div > div.col-md-12 > div:nth-child(1) > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(1) > div > div.row.product-item-image-xs").click()
        # print WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div:nth-child(11) > div > div > div.col-lg-10.col-sm-9.col-xs-12 > div:nth-child(2) > div > div.col-md-12 > div:nth-child(1) > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(1) > div"))).get_attribute("innerHTML")
        # WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-list-container > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(1) > div > div.product-description.row > div.product-item-item.hyperlink-like"))).click()
        while True:
            try:
                # WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-list-container > div:nth-child(7) > div:nth-child(2) > div > div:nth-child(1) > div > div.product-item-image.row"))).click()
                ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#product-list-container > div:nth-child(7) > div:nth-child(2)")).perform()
                self.time.sleep(1)
                WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-list-container > div:nth-child(7) > div:nth-child(2)"))).click()
                self.time.sleep(1)
                print "**Success item search**.\n"
                return None
            except:
                return None


