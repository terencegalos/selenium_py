from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from helper.table_gateway import gateway
from helper.domainobject import domainobject

from tqdm import tqdm

class wingtai(domainobject):
    
    
    def __init__(self,driver,scraper_mode):
        super().__init__(driver)
        self.mode = scraper_mode

    vendor = "Wing Tai Trading"
    home = "https://wingtai.solovue.com/"
    uname = "service@waresitat.com"
    passw = "wingtaiinventory@4"
    login = "http://www.wtcollectionshowroom.com/cgi-wtcollectionshowroom/sb/order.cgi?func=2&storeid=*1209f4a48ae200708d5090&html_reg=html"
    delay = 1
    links = []
    
        
    def nextPage(self):
        print("Pagination attempt...")
        try:
            self.driver.driver.find_elements(By.CSS_SELECTOR,"input[value=Next]")[-1].click()
            self.time.sleep(1)
            return True
        except:
            print("Page exhausted..")
            return False

    def get_cats(self):
        ln = [l.get_attribute("href") for l in self.links.extself.driver.driver.find_elements(By.CSS_SELECTOR,"#loopproducts > div > div.loopprod.center > div.prodbasics > a") if l.get_attribute("href") not in self.links]
        ln = [l.get_attribute("href") for l in self.links.extself.driver.driver.find_elements(By.CSS_SELECTOR,"#ShopSite > li:nth-child(2) > div > ul > li:nth-child(1) > a") if l.get_attribute("href") not in self.links]
        print(ln)
        return ln

    def get_all_items(self):
        print("Getting all items...")
        self.driver.get(self.home)
        self.time.sleep(1)
        cats = self.get_cats()
        for cat in cats:
            self.driver.get(cat)
            self.time.sleep(1)
            self.get_info()
            while self.nextPage():
                self.get_info()


    def init_login(self,un,pw):
        self.driver.get(self.home)
        self.time.sleep(2)
        self.driver.find_element(By.XPATH,'//*[@id="pre-login-navbar"]/li[5]/a').click()
        self.time.sleep(1)
        
        print("Logging in.")
        self.driver.find_element(By.ID,"username").send_keys(un)
        self.driver.find_element(By.ID,"password").send_keys(pw)
        self.driver.find_element(By.ID,"password").send_keys(Keys.ENTER)
        # self.driver.find_element(By.CSS_SELECTOR,"#Sign\20 In").click()
        self.time.sleep(8)
        print("Success.")

    def get_info_orig(self,sku=None):
        page_items = []
        print("Initiate grabbing items...")
        page_items.extend(self.save_info())
        while self.nextPage():
            page_items.extend(self.save_info())
        for page in page_items:
            print(type(page))
        
        self.time.sleep(2)
        return page_items

    def get_info(self,sku=None):
        
        # self.driver.find_element(By.XPATH,'//*[@id="filter-list"]/ul[1]/li/div[2]').click()
        self.driver.find_element(By.XPATH,'/html/body/div[11]/div/div/div[1]/div/div[2]/ul/li/ul[4]/li/div[2]').click()
        field_stones_nav = self.driver.find_elements(By.XPATH,'/html/body/div[11]/div/div/div[1]/div/div[2]/ul/li/ul[4]/li/ul/li/div[2]')
        dbs = []
        for nav in field_stones_nav:
            nav.click()
            self.time.sleep(2)
        
            self.time.sleep(5)
            # def loop_items():
            #     records = []
            #     item_obj = self.driver.find_elements(By.XPATH,'//*[@id="product-list-container"]/div[6]/div')
            #     for idx,obj in enumerate(item_obj,start=1):
            #         print(f"Index: {idx}")
            #         records.append(self.get_info(obj))
                
            #     return records
            
            
            last_height = self.driver.execute_script('return document.body.scrollHeight;')
            
            while True:
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                self.time.sleep(2)
                new_height = self.driver.execute_script('return document.body.scrollHeight;')
                if last_height == new_height:
                    break
                last_height = new_height
            
            # records = loop_items()
            # if records:
            #     return records
            # return None
            
            # print "Status: Looping each items"
            item_obj = self.driver.find_elements(By.XPATH,'//*[@id="product-list-container"]/div[6]/div')
            for idx,obj in enumerate(item_obj,start=1):
                print(f"Index: {idx}")
                # records.append(self.get_info(obj))
            
            # items = self.driver.driver.find_elements(By.CSS_SELECTOR,"div[id^='loop'] > div")
            
            # for item in items:
                
                db = gateway()
                # print(f"Object: {obj.text}")
                try:
                    db.name = obj.find_element(By.XPATH,'div/div[1]/div/div[2]/div[1]').text
                    if not db:
                        return
                    # print(db.name)
                    # print(obj.get_attribute('innerText'))
                except:
                    print("Skipping. Possible noise.")
                    print("innerHTML: \n",obj.get_attribute('innerText'))
                    # db.name = ""
                    # continue #its possible that you'll get error from noise. Just skip and move to next div
                
                try:
                    db.sku = obj.find_element(By.XPATH,'div/div[1]/div/div[2]/div[2]').text
                except:
                    # print self.driver.get_attribute("innerHTML")
                    db.sku = ""
                    # continue #possible noise
                
                db.cat = "" 
                db.desc = ""

                try:
                    db.stock = obj.find_element(By.XPATH,'div/div[1]/div/div[2]/div[5]/table/tbody/tr[1]/td[4]/img').get_attribute('title')
                except:
                    db.stock = ""

                db.sale = ""
                db.set = ""
                db.custom = ""
                db.size = ""
                db.seller = ""

                try:
                    db.min1 = obj.find_element(By.XPATH,'div/div[1]/div/div[2]/div[4]/div/table/tbody/tr[1]/td[5]/span').text.strip('Qty ')
                    if "-" in db.min1:
                        db.min1 = db.min1.split("-")[0].strip()
                    db.price1 = obj.find_element(By.XPATH,'div/div[1]/div/div[2]/div[4]/div/table/tbody/tr[1]/td[2]/span').text.strip("$")

                except:
                    db.min1 = ""
                    db.price1 = ""

                try:
                    db.min2 = obj.find_element(By.XPATH,'div/div[1]/div/div[2]/div[4]/div/table/tbody/tr[2]/td[5]/span').text.strip('Qty ')
                    if "+" in db.min2:
                        db.min2 = db.min2.strip("+").strip()
                    if "-" in db.min2:
                        db.min2 = db.min2.split("-")[0].strip()
                    db.price2 = obj.find_element(By.XPATH,'div/div[1]/div/div[2]/div[4]/div/table/tbody/tr[2]/td[2]/span').text.strip("$")

                except:
                    db.min2 = ""
                    db.price2 = ""

                try:
                    db.min3 = obj.find_element(By.XPATH,'div/div[1]/div/div[2]/div[4]/div/table/tbody/tr[3]/td[5]/span').text.strip("Qty ")
                    if "-" in db.min3:
                        db.min3 = db.min3.split("-")[0].strip().strip("+")
                    if "+" in db.min3:
                        db.min3 = db.min3.strip().strip("+")
                    db.price3 = obj.find_element(By.XPATH,'div/div[1]/div/div[2]/div[4]/div/table/tbody/tr[3]/td[2]/span').text.strip("$")

                except:
                    db.min3 = ""
                    db.price3 = ""

                db.multi = db.min1
                db.dir400 = "WingTai400"
                db.dir160 = "WingTai160"

                try:
                    db.img400 = obj.find_element(By.XPATH,'div/div[1]/div/div[1]/img').get_attribute("src")

                except:
                    print("Image not found. Placing dummy image url.")
                    db.img400 = "http://www.wtcollectionshowroom.com/store/media/noimage.jpg"

                db.img160 = db.img400.split("/")[-1:][0]
                db.desc2 = ""
                db.option = ""
                db.dir800 = "WingTai800"
                db.img800 = db.img160
                print(db)
                dbs.append(db)

        return dbs
        
        
    def search_item(self,row):
        
        # def loop_items():
        #     records = []
        #     item_obj = self.driver.find_elements(By.XPATH,'//*[@id="product-list-container"]/div[6]/div')
        #     for idx,obj in enumerate(item_obj,start=1):
        #         print(f"Index: {idx}")
        #         records.append(self.get_info(obj))
            
        #     return records
        
        # self.driver.find_element(By.XPATH,'//*[@id="filter-list"]/ul[1]/li/div[2]').click()
        
        # self.time.sleep(5)
        
        # last_height = self.driver.execute_script('return document.body.scrollHeight;')
        
        # while True:
        #     self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        #     self.time.sleep(2)
        #     new_height = self.driver.execute_script('return document.body.scrollHeight;')
        #     if last_height == new_height:
        #         break
        #     last_height = new_height
        
        # records = loop_items()
        # if records:
        #     return records
        return None
        
        # while True:
        #     try:
        #         print("\nSearching for item: " + row+"\n")
        #         self.driver.find_element(By.NAME,"search_field").clear()
        #         self.driver.find_element(By.NAME,"search_field").send_keys(str(row))
        #         self.driver.find_element(By.NAME,"search_field").send_keys(self.Keys.ENTER)
        #         self.time.sleep(2)
        #         break
        #     except:
        #         self.driver.get(self.home)
        #         self.time.sleep(1)
        #         continue
        # try:
        #     item = self.driver.find_element(By.CSS_SELECTOR,"#bb-loopproducts > li > div.item")
        #     return None
        # except:
        #     return (["https://www.wtcollectionshowroom.com/store/"+row+"_moreinfo.html"])