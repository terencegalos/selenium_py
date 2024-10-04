from helper.table_gateway import gateway
import helper.domainobject as domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class dns(domainobject.domainobject):
    
    def __init__(self,driver,scraper_mode):
        super().__init__(driver)
        self.mode = scraper_mode

    vendor = "DNS Designs"
    url = "http://www.dnsdesignsandmore.com/index.php"
    home = "http://www.dnsdesignsandmore.com/index.php"
    login = "http://www.dnsdesignsandmore.com/index.php?route=account/login"
    sitemap = "https://www.dnsdesignsandmore.com/index.php?route=information/sitemap"
    uname = "rstuart"
    passw = "rstuart321"
    delay = 1
    allitems = []
    lastPage = ""
    stopFlag = False
    links = []
    
        
    def nextPage(self,num):
        print(f"Page num: {num}")
        self.driver.get(f"https://www.dnsdesignsandmore.com/shop/?q=%20&catslug=undefined&activepage={num}")
        self.time.sleep(2)
        
    def get_cat_items(self):
        self.driver.get("https://www.dnsdesignsandmore.com/index.php?route=information/sitemap")
        self.time.sleep(1)
        # scat = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR,"#content > div.sitemap-info > div.left > ul > li > a")]
        scat = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR,"#content > div.sitemap-info > div.left  a")]
        for c in scat:
            # try:
            print("***********************")
            print(c)
            self.driver.get(c)
            self.time.sleep(1)

            item = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR,"div.name a")]
            print(item)
            self.allitems.extend(item)

            while self.nextPage():
                item = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR,"div.name a")]
                print(list(item))
                self.allitems.extend(list(item))
                print(item)
        return self.allitems

    def init_login(self,un,pw):
        self.driver.get(self.login)
        
        print("Logging in.")
        self.driver.find_element(By.XPATH,'//*[@id="navigation"]/div/div[2]/div/ul/li[1]/div').click()
        self.time.sleep(0.5)
        self.driver.find_element(By.XPATH,'//*[@id="navigation"]/div/div[2]/div/ul/li[1]/ul/li[1]/a').click()
        self.time.sleep(0.5)
        self.driver.find_element(By.NAME,"email").send_keys(un)
        self.driver.find_element(By.NAME,"pass").send_keys(pw)
        input("handle captcha? [y/n]")
        self.driver.find_element(By.NAME,"pass").send_keys(Keys.ENTER)
        print("Success.")


    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(5) > div > div > div > form > div > h3").text
        db.sku = self.driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(5) > div > div > div > form > div > p:nth-child(3)").text
        db.cat = ""#"|".join([i.text.encode("utf-8") for i in self.driver.find_elements(By.CSS_SELECTOR,"div.breadcrumb a")])
        db.desc = ""
        db.stock = self.driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(5) > div > div > div > form > div > div:nth-child(13) > p").text
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(5) > div > div > div > form > div > p:nth-child(5)").text
        db.seller = ""
        db.min1 = self.driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(5) > div > div > div > form > div > table > tbody > tr:nth-child(1) > td:nth-child(2)").text
        db.price1 = self.driver.find_element(By.CSS_SELECTOR,"#varprice").text
        try:
            db.min2 = self.driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(5) > div > div > div > form > div > table > tbody > tr:nth-child(2) > td:nth-child(2)").text
            db.price2 = self.driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(5) > div > div > div > form > div > table > tbody > tr:nth-child(2) > td:nth-child(1)").text
        except:
            db.min2 = ""
            db.price2 = ""
            
        try:
            db.min3 = self.driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(5) > div > div > div > form > div > table > tbody > tr:nth-child(3) > td:nth-child(2)').text
            db.price3 = self.driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(5) > div > div > div > form > div > table > tbody > tr:nth-child(3) > td:nth-child(1)').text
        except:
            db.min3 = ""
            db.price3 = ""
        db.multi = db.min1
        db.dir400 = "DNS400"
        db.dir160 = "DNS160"
        try:
            db.img400 = self.driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(5) > div > div > div > div > div > div > a").get_attribute("href")
        except Exception as e:
            print(e)
            self.time.sleep(3)
            return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = self.driver.current_url
        db.option = ""
        db.dir800 = "DNS800"
        db.img800 = db.img160
        print(db)
        return(db)
        
        
    def search_item(self,row):
        self.allitems = []
        print("\nSearching for item: " + row+"\n")
        while True:
            try:
                self.driver.find_element(By.NAME,"q").clear()
                self.driver.find_element(By.NAME,"q").send_keys(str(row))
                self.driver.find_element(By.NAME,"q").send_keys(Keys.ENTER)
                self.time.sleep(self.delay)
                break
            except:
                self.driver.get(self.url)
                self.time.sleep(self.delay)
                continue

        item = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR,"#listedproduct > div > form > div > h5 > a")]
        print(item)
        self.allitems.extend(item)
        # total_page = int(self.driver.find_element(By.CSS_SELECTOR,"#appndHtml > div.full_Div.text-center > ul > li:nth-child(5) > a").get_attribute("id"))
        # for page_num in range(total_page):
        #     self.nextPage(page_num)
        #     item = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR,"#listedproduct > div > form > div > h5 > a")]
        #     self.allitems.extend(item)
        #     print(item)
        
        return self.allitems


