from helper.table_gateway import gateway
from helper.domainobject import domainobject
import datetime,csv

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class ragon(domainobject):
    
    def __init__(self,driver,scraper_mode):
        super().__init__(driver)
        self.mode = scraper_mode

    vendor = "Ragon House Collection"
    url = "http://ragonhouse.com/"
    home = "http://ragonhouse.com/"
    login = "https://ragonhouse.com/login.php"
    uname = "rick@waresitat.com"
    passw = "ragonhouse1"
    lastStop =  "https://ragonhouse.com/holiday-and-winter/15.5-cedar-and-hemlock-bush.html"
    sitemap = 'https://ragonhouse.com/collections/'
    flag = False
    delay = 1
    counter = 190
    items = []
    links = []

    def export_all_product_urls(self, items):
        with open('./csv/outfile/' + self.vendor + '_product_urls.csv','wb') as ragon_file:
            writer = csv.writer(ragon_file)
            for item in items:
                writer.writerow([item])

    def nextPage(self):
        # try:
        #     # self.driver.find_element(By.XPATH,'//*[@id="product-listing-container"]/nav/ul/li[7]/a').click()
        #     self.driver.find_element(By.CSS_SELECTOR,'#product-listing-container > nav > ul > li.pagination-item.pagination-item--next > a').click()
        #     self.time.sleep(3)
        #     return True
        # except:
        #     return False
        for x in range(self.counter,0,-1):
            self.driver.get("https://ragonhouse.com/collections/?page={}".format(x))
            self.time.sleep(1)
            self.counter -= 1
            if self.counter > 0:
                return True

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#sw_dropdown_2878 > a")).perform()
        # self.time.sleep(1)
        self.driver.find_element(By.XPATH,"/html/body/header/nav/ul/li[3]/a[1]").click()
        self.time.sleep(1)
        # self.driver.find_element(By.CSS_SELECTOR,"#account_info_2878 > div.ty-account-info__buttons.buttons-container > a.cm-dialog-opener.cm-dialog-auto-size.ty-btn.ty-btn__secondary").click()

        # self.time.sleep(1)
        print("Logging in...")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login_email"))).send_keys(un)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login_pass"))).send_keys(pw)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login_pass"))).send_keys(Keys.ENTER)
        self.time.sleep(3)
        print("Success.")

    def get_info(self,item=None):
        db = gateway()
        db.name = (self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > div > div.productView > section.productView-details.product-data > div > h1").text)

        db.sku = self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > div > div.productView > section.productView-details.product-data > div > dl.productView-custom > dd").text
        db.cat = "|".join([c.text for c in self.driver.find_elements(By.CSS_SELECTOR,"#main-content > div.container > nav > ol > li.breadcrumb > a > span")])
        try:
            db.desc = self.driver.find_element(By.CSS_SELECTOR,"#tab-description").text
        except:
            db.desc = ""
        try:
            db.stock = self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > div > div.productView > section.productView-details.product-data > div > div.productView-availability > dd").text
        except:
            db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > div > div.productView > section.productView-details.product-data > div > div.productView-dimensions").text
        db.seller = ""
        try:
            db.min1 = self.driver.find_element(By.XPATH,'//*[@id="qty[]"]').get_attribute('value')
        except:
            db.min1 = ""
        try:
            db.price1 = self.driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div/div[1]/section[2]/div/div[1]/div[3]/span[3]').text
        except:
            db.price1 = ""
        try:
            db.min2 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty-discount > table > thead > tr > th:nth-child(3)").text.strip("+")
        except:
            db.min2 = ""
        try:
            db.price2 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty-discount > table > tbody > tr > td:nth-child(3) > bdi > span").text
        except:
            db.price2 = ""
        try:
            db.min3 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty-discount > table > thead > tr > th:nth-child(4)").text.strip("+")
        except:
            db.min3 = ""
        try:
            db.price3 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty-discount > table > tbody > tr > td:nth-child(4) > bdi > span").text
        except:
            db.price3 = ""
        try:
            db.multi = self.driver.find_element(By.XPATH,'//*[@id="qty[]"]').get_attribute('value')
        except:
            db.multi = ""
        db.dir400 = "Ragon400"
        db.dir160 = "Ragon160"
        #ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#fancybox-wrap")).perform()
        #self.time.sleep(1)
        try:
            db.img400 = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div.container > div > div.productView > section.productView-images > figure > div > a"))).get_attribute("href")
        except:
            return
        db.img160 = db.img400.split("/")[-1:][0]
        try:
            db.desc2 = self.driver.find_element(By.CSS_SELECTOR,"#content_description").text
        except:
            db.desc2 = ""
        db.option = ""
        db.dir800 = "Ragon800"
        db.img800 = db.img160
        print(db)
        self.time.sleep(1)
        return db


    def search_item(self,row=None):


        self.items = []
        if row:
            print("\nSearching for item: " + row+"\n")
            while True:
                try:
                    self.driver.find_element(By.CSS_SELECTOR,"#quick-search-expand").click()
                    self.time.sleep(1)
                    self.driver.find_element(By.NAME,"nav-quick-search").clear()
                    self.driver.find_element(By.NAME,"nav-quick-search").send_keys(row)
                    self.driver.find_element(By.NAME,"nav-quick-search").send_keys(Keys.ENTER)
                    self.time.sleep(1)
                    # self.driver.get("https://ragonhouse.com/index.php?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&q=+&dispatch=products.search&page=16")
                    break
                except Exception as e:
                    print(e)
                    self.driver.refresh()
                    self.time.sleep(1)
                    continue
        else:
            self.driver.get(self.sitemap)
            self.time.sleep(1)

        item = [a.get_attribute("href") for a in self.driver.find_elements(By.XPATH,'//*[@id="product-listing-container"]/div[1]/ul/li[1]/article/div/h3/a')]
        print(item)

        self.items.extend(item)

        # while self.nextPage():
        #     item = [a.get_attribute("href") for a in self.driver.find_elements(By.XPATH,'//*[@id="product-listing-container"]/div[1]/ul/li[1]/article/div/h3/a')]
        #     print(item)
        #     self.items.extend(item)

        return self.items
