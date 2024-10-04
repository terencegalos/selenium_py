from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class acg(domainobject):

    vendor = "A Cheerful Giver"
    url = "https://www.acheerfulgiver.com/"
    home = "https://www.acheerfulgiver.com/"
    uname = "kaye.williams@waresitat.com"
    passw = "b2bonline"
    delay = 1
    links = []
    skus = []
    cats = []
        
    def get_cats(self):
        cat = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR,"body > div.wrapper.ps-static.en-lang-class > div > div.main-container.col1-layout > div > div > div > div.page-sitemap > ul.sitemap > li > a")]
        print(cat)
        self.cats.extend(cat)

    def get_sku_links(self):
        for sku in self.skus:
            link = self.search_item(sku)
            print(link)
            self.links.extend(link)

    def nextPage(self):
        try:
            self.driver.find_elements(By.CSS_SELECTOR,"a[title='Next']")[-1].click()
            return True
        except:
            print("\nPage exhausted.\n")
            self.time.sleep(3)
            return False

    def get_page_skus(self):
        sku = [tr.find_element(By.CSS_SELECTOR,"td:nth-child(3)").text for tr in self.driver.find_elements(By.CSS_SELECTOR,"#super-product-table > tbody > tr")[1:] if tr.find_element(By.CSS_SELECTOR,"td:nth-child(3)").text not in self.skus]
        print(sku)
        self.skus.extend(sku)

    '''
    scraper mode:
        -get skus first
        -get links by searching using grabbed skus
    '''
    def get_all_items(self):
        print("Scraper mode:")
        self.driver.get("https://www.acheerfulgiver.com/catalog/seo_sitemap/product/")
        self.time.sleep(1)

        
        self.get_cats()
        while self.nextPage():
            self.get_cats()

        print("Getting skus...")
        for cat in self.cats:
            print(cat)
            self.driver.get(cat)
            self.get_page_skus()

        

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#newsletterpopup div div button span:nth-child(1) i"))).click()
        # self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element(By.NAME,"email").send_keys(un)
        # self.driver.find_element(By.NAME,"password").send_keys(pw)
        # self.driver.find_element(By.NAME,"password").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div.column.main > div.product-info-main > div.page-title-wrapper.product > h1 > span").text.encode("utf-8")
        db.sku = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div.column.main > div.product-info-main > div.product-info-price > div.product-info-stock-sku > div.product.attribute.sku > div").text.encode("utf-8")
        db.cat = ""

        try:
            db.desc = self.driver.find_element(By.CSS_SELECTOR,"#description > div > div").text.encode("utf-8")
        except:
            db.desc = ""

        try:
            db.stock = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div.column.main > div.product-info-main > div.product-info-price > div.product-info-stock-sku > div.stock.available > span").text.split()[1]
        except:
            db.stock = "In stock"

        db.sale = ""
        db.set = ""
        db.custom = self.driver.current_url
        db.size = ""
        db.seller = ""
        db.min1 = 1
        db.price1 = 99
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "ACG400"
        db.dir160 = "ACG160"
        # db.img400 = self.driver.find_element(By.CSS_SELECTOR,"#magnifier-item-0").get_attribute("src")
        self.time.sleep(5)
        while True:
            try:
                # db.img400 = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#magnifier-item-0"))).get_attribute("src")
                db.img400 = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#magnifier-item-0"))).get_attribute("src")
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                continue
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "ACG800"
        db.img800 = db.img160
        print(db)
        return db
        
        
    def search_item(self,row):
        
        print("\nAction: Searching for item: " + row+"\n")
        # while True:
        #     try:
        self.driver.find_element(By.XPATH,'//*[@id="section-announcement"]/div/div/div[3]/a[2]').click()
        self.time.sleep(1)
        self.driver.find_element(By.NAME,"q").clear()
        self.driver.find_element(By.NAME,"q").send_keys(row)
        self.driver.find_element(By.NAME,"q").send_keys(Keys.ENTER)
        self.item = row.strip()
        self.time.sleep(1)
            #     break
            # except:
            #     self.driver.refresh()
            #     self.time.sleep(1)
            #     continue

        try:
            # self.driver.find_element(By.CSS_SELECTOR,"#limiter option:nth-child(3)").click()
            # self.time.sleep(1)
            items = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"#maincontent > div.columns > div.column.main > div.search.results > div.products.wrapper.grid.products-grid > ol > li > div > div > strong > a")]
            return items
        except:
            return None
