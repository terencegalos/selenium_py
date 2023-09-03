from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class blossom(domainobject.domainobject):

    vendor = "Blossom Bucket"
    url = "https://gift.wholesale.crossroadsfamily.com/blossom-bucket-shop/shop-blossom-bucket/?Vendor=BLOSSOMBUCKET&orderBy=-Id&context=shop&page=1"
    search = "https://gift.wholesale.crossroadsfamily.com/blossom-bucket-shop/shop-blossom-bucket/?Vendor=BLOSSOMBUCKET&orderBy=-Id&context=shop&page=1"
    home = "https://gift.wholesale.crossroadsfamily.com/blossom-bucket-shop/shop-blossom-bucket/?Vendor=BLOSSOMBUCKET&orderBy=-Id&context=shop&page=1"
    lastStop = "https://gift.wholesale.crossroadsfamily.com/blossom-bucket-shop/shop-blossom-bucket/218-20212?position=-1"
    flag = False
    uname = "rick@waresitat.com"
    passw = "B2T1K6"
    delay = 1
    links = []
    
        
    def init_login(self,un,pw):
        self.driver.get(self.search)
        self.time.sleep(1)
        # self.driver.find_element_by_css_selector("#site > header > div > div > div.navigation > div > nav > ul:nth-child(2) > li:nth-child(3) > a").click()
        # self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_css_selector("div > div > div > div > div > div:nth-child(1) > div > div > login > form > login-fieldset > div:nth-child(1) > div > div > div > div:nth-child(1) > div > input").send_keys(un)
        # self.driver.find_element_by_css_selector("div > div > div > div > div > div:nth-child(1) > div > div > login > form > login-fieldset > div:nth-child(2) > div > div > div > div:nth-child(1) > div > input").send_keys(pw)
        # self.driver.find_element_by_css_selector("div > div > div > div > div > div:nth-child(1) > div > div > login > form > login-fieldset > div:nth-child(2) > div > div > div > div:nth-child(1) > div > input").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def nextPage(self):
        print "Execute pagination."
        while True:
            status = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"ui-view > shopping-container > div > ui-view > shopping-multi-view > div > div.col-xl-9.col-lg-8.col-md-7 > auto-query-header > div > div.pull-left > div > span"))).text
            if "loading" in status.lower():
                self.time.sleep(1)
                continue
            else:
                break
            
        status = status.split()
        print status
        print status[-1]
        print status[-3]
        if float(status[-1]) > float(status[-3]):
            # WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#wide-col > div > div > ui-view > shopping-container > div > ui-view > shopping-multi-view > div > div.col-xl-9.col-lg-8.col-md-7 > auto-query-footer > div > div.m-y-1.clearfix > div.pull-left > div > li.pagination-next.ng-scope > a"))).click()
            WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#wide-col > div > div > ui-view > shopping-container > div > ui-view > shopping-multi-view > div > div.col-xl-9.col-lg-8.col-md-7.filters-open.multi-view-right > auto-query-footer > div > div.m-y-1.clearfix > div.pagination.inline-block.valign-middle > div > li.pagination-next.ng-scope > a"))).click()
            self.time.sleep(2)
            return True
        else:
            print "Page exhausted."
            return False

    def extract_urls(self):
        ln = [item.get_attribute("href") for item in self.driver.find_elements_by_css_selector("div > shopping-grid > div > shopping-item-image > a")]
        print ln
        return ln

    def get_links(self):
        print "Initializing scraper. Getting all items in this vendor..."
        self.driver.get("https://www.blossombucket.com/shop/")
        self.time.sleep(10)
        self.links.extend(self.extract_urls())
        while self.nextPage():
            self.links.extend(self.extract_urls())

        print "Done."


    def get_info(self,item=None):
        db = gateway()
        self.time.sleep(1)
        while True:
            try:
                self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div > div.col-sm-6.col-md-5 > message-icon > div > div").text.encode("utf-8")
                print "Loading..."
                self.driver.refresh()
                self.time.sleep(5)
                continue
            except:
                break
                
        try:
            db.name = WebDriverWait(self.driver,1).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"ui-view > shopping-container > div > ui-view > shopping-one-up > div > div:nth-child(2) > shopping-one-up-above-image > div > h1"))).text.encode("utf-8")
        except:
            return
        db.sku = self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div > div:nth-child(2) > div.col-xs-12.col-sm-7.col-md-5 > shopping-one-up-details > div:nth-child(1) > strong").text.encode("utf-8")
        db.cat = ""#self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div.ng-scope > div.row.ng-scope > div.col-xs-12.col-sm-5.col-md-5 > shopping-one-up-details > div:nth-child(4) > strong").text.encode("utf-8")
        try:
            db.desc = self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div.ng-scope > div.row.ng-scope > div.col-xs-12.col-sm-5.col-md-5 > shopping-one-up-details > div:nth-child(6) > strong").text.encode("utf-8")
        except:
            db.desc = ""
        try:
            db.stock = self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div.ng-scope > div.row.ng-scope > div.col-xs-12.col-sm-5.col-md-5 > shopping-one-up-heading > div.detail-item.ng-scope > strong").text.encode("utf-8")
        except:
            db.stock = ""
        try:
            db.sale = self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div.ng-scope > div.row.ng-scope > div.col-xs-12.col-sm-5.col-md-5 > shopping-one-up-heading > div:nth-child(3) > div > p > span").text.encode("utf-8")
        except:
            db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div > div:nth-child(2) > div.col-xs-12.col-sm-7.col-md-5 > shopping-one-up-details > div:nth-child(3) > strong").text.encode("utf-8")
        db.seller = ""
        # try:
        db.min1 = 1#self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div.ng-scope > div.row.ng-scope > div.col-xs-12.col-sm-5.col-md-5 > shopping-price-breaks > div > div > div:nth-child(2) > div:nth-child(1)").text.encode("utf-8")
        # except:
        #     return
        try:
            db.price1 = self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div.ng-scope > div.row.ng-scope > div.col-xs-12.col-sm-5.col-md-5 > shopping-price-breaks > div > div > div:nth-child(2) > div:nth-child(2)").text.encode("utf-8")
        except:
            db.price1 = 99

        db.min2 = ""#self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div.ng-scope > div.row.ng-scope > div.col-xs-12.col-sm-5.col-md-5 > shopping-price-breaks > div > div > div:nth-child(3) > div:nth-child(1)").text.encode("utf-8")
        db.price2 = ""#self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div.ng-scope > div.row.ng-scope > div.col-xs-12.col-sm-5.col-md-5 > shopping-price-breaks > div > div > div:nth-child(3) > div:nth-child(2)").text.encode("utf-8")
        db.min3 = ""#self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div.ng-scope > div.row.ng-scope > div.col-xs-12.col-sm-5.col-md-5 > shopping-price-breaks > div > div > div:nth-child(4) > div:nth-child(1)").text.encode("utf-8")
        db.price3 = ""#self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div.ng-scope > div.row.ng-scope > div.col-xs-12.col-sm-5.col-md-5 > shopping-price-breaks > div > div > div:nth-child(4) > div:nth-child(2)").text.encode("utf-8")
        db.multi = db.min1#self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div.ng-scope > div.row.ng-scope > div.col-xs-12.col-sm-5.col-md-5 > shopping-price-breaks > div > div > div:nth-child(2) > div:nth-child(1)").text.encode("utf-8")
        db.dir400 = "Blossom400"
        db.dir160 = "Blossom160"
        db.img400 = self.driver.find_element_by_css_selector("ui-view > shopping-container > div > ui-view > shopping-one-up > div > div:nth-child(2) > div.col-xs-12.col-sm-5.col-md-7 > product-images > section > div > div.main-images-box.text-center > div > div:nth-child(1) > a").get_attribute("ng-href")
        db.img160 = db.img400.split("/")[-1:][0] #if ".jpg?" not in db.img400.split("/")[-1:][0] else (db.img400.split("/")[-1:][0]).split("?")[0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Blossom800"
        db.img800 = db.img160
        print db
        # self.time.sleep(3) # delay after print
        return db
        
        
    def search_item(self,row):
        self.links = []
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.time.sleep(1)
                inp = self.driver.find_element_by_css_selector("input[type=text]")
                inp.clear()
                inp.send_keys(row)
                inp.send_keys(Keys.ENTER)

                self.time.sleep(1)
                break
            except Exception as e:
                print "Search failed:"
                self.driver.get(self.search)
                print e
                self.time.sleep(1)
                continue

        
        print "Searching for results..."
        while True:
            status = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"ui-view > shopping-container > div > ui-view > shopping-multi-view > div > div.col-xl-9.col-lg-8.col-md-7.filters-open.multi-view-right > auto-query-header > div > div:nth-child(3) > div > span"))).text
            if "loading" in status.lower():
                self.time.sleep(1)
            else:
                break
        try:

            items = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#wide-col > div > div > ui-view > shopping-container > div > ui-view > shopping-multi-view > div > div.col-xl-9.col-lg-8.col-md-7.filters-open.multi-view-right > div > shopping-multi-view-cards > div > div > a.ng-scope") if "http" in a.get_attribute("href")]
            if len(items) < 1:
                print "No item found."
                raise

            print items
            self.links.extend(items)

            while self.nextPage():
                items = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#wide-col > div > div > ui-view > shopping-container > div > ui-view > shopping-multi-view > div > div.col-xl-9.col-lg-8.col-md-7.filters-open.multi-view-right > div > shopping-multi-view-cards > div > div > a.ng-scope")]
                if len(items) < 1:
                    print "No item found."
                    raise

                print items
                self.links.extend(items)

            return self.links


        except:
            print "Item not found."
            return None