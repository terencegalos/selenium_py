from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class janmichael(domainobject):

    def __init__(self,driver,mode):
        self.driver = driver
        self.mode = mode

    vendor = "JanMichael's Crafts"
    url = "https://www.janmichaelsartandhome.com/"
    home = "https://www.janmichaelsartandhome.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    links = []
    
        
    def nextPage(self):
        try:
            next_btn = self.driver.find_element(By.CSS_SELECTOR,"#product-listing-container > div:nth-child(1) > div.product-listing-filter-left.show > div.product-listing-pagination.show > nav > ul > li.pagination-item.pagination-item--next > a").get_attribute('href')
            self.driver.get(next_btn)
            self.time.sleep(1)
            return True
        except:
            print("Page exhausted.")
            return False

    def get_links(self):
        ln = [l.get_attribute("href") for l in self.driver.find_elements(By.CSS_SELECTOR,"#product-listing-container > div.product-view-mode > form > ul.productGrid.is-open > li a") if l.get_attribute("href") not in self.links] # will get return emtpy if already
        print(f'Links:{" ".join(ln)}')
        return ln

    def get_all_items(self,cat_num):
        print("Extracting links from sitemap...")
        self.driver.get("https://www.janmichaelsartandhome.com/sitemap/categories/") #navigate categories
        self.time.sleep(1) #delay 1 sec for page to load

        #get all category links and loop each and navigate
        cats = [cat.get_attribute("href") for cat in self.driver.find_elements(By.CSS_SELECTOR,"body > div.body > div.container > ul > li > ul > li > a")[:int(cat_num)]]# 
        print(f'Categories: {" ".join(cats)}')
        for cat in cats:
            self.driver.get(cat)
            self.time.sleep(1)
            self.links.extend(self.get_links())
            while self.nextPage():
                self.links.extend(self.get_links())

    def init_login(self,un,pw):
        self.driver.get("https://www.janmichaelsartandhome.com/login.php")
        self.time.sleep(1)
        # WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > header > div.navPages-section.navPages-section-3 > nav > ul > li.navUser-item.navUser-item--account > a"))).click()
        # self.time.sleep(1)
        # WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#account-preview-dropdown > div > ul > li:nth-child(2) > a"))).click()
        # self.time.sleep(1)
        
        print("Logging in.")
        self.driver.find_element(By.ID,"login_email").send_keys(un)
        self.driver.find_element(By.ID,"login_pass").send_keys(pw)
        self.driver.find_element(By.ID,"login_pass").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print("Success.")
    
    #This is used for click options if available then save info 
    def clickbtn(self,btn):
        opt = []
        optcount = len(btn.find_elements(By.CSS_SELECTOR,"option"))

        for x in range(1,optcount):
            btn = self.driver.find_element(By.CSS_SELECTOR,"select.form-select:nth-child(2)")
            try:
                btn.find_elements(By.CSS_SELECTOR,"option")[x].click()
                db = self.save_info(btn.find_elements(By.CSS_SELECTOR,"option")[x].text if "Frame" in btn.find_elements(By.CSS_SELECTOR,"option")[x].get_attribute("innerHTML") else "")
                self.time.sleep(2)
                print("Option selected.")
                opt.append(db)
            except:
                continue

        return opt
    
    def selectbtn(self,btn):
        opt = []
        optcount = len(btn.find_elements(By.CSS_SELECTOR,"label.form-option"))

        for x in range(optcount):
            btn = self.driver.find_element(By.CSS_SELECTOR,"div.form-field[data-product-attribute=set-rectangle]")
            # print btn.get_attribute("innerHTML")
            try:
                btn.find_elements(By.CSS_SELECTOR,"label.form-option")[x].click()
                db = self.save_info(btn.find_elements(By.CSS_SELECTOR,"label.form-option")[x].text)
                self.time.sleep(2)
                print("Option selected.")
                opt.append(db)
            except:
                continue

        return opt
        
    #Special for Janmichaels in case options are available
    def get_info(self,item=None):
    
        option = []
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR,"select.form-select:nth-child(2)")
            print("Btn detected.")
            db = self.clickbtn(btn)
            option.extend(db) #returns a list of items
        except:
            try:
                btn = self.driver.find_element(By.CSS_SELECTOR,"div.form-field[data-product-attribute=set-rectangle]")
                print("Btn detected.")
                db = self.selectbtn(btn)
                option.extend(db) #returns a list of items
            except:
                print("Btn not found.")
                db = self.save_info()
                option.append(db)
            
        return option
    
    def save_info(self,opt=""):
        db = gateway()

        db.name = self.driver.find_element(By.CSS_SELECTOR,"h1").text.encode("utf-8")

        try:
            db.sku = WebDriverWait(self.driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div.body > div.container > div > div.productView > section:nth-child(3) > div.productView-info > dl:nth-child(1) > dd"))).text.encode("utf-8")
        except:
            print("No sku detected. Stopping.")
            return
        
        db.cat = opt

        try:
            db.desc = self.driver.find_element(By.CSS_SELECTOR,"#tab-description > p").text.encode("utf-8")
        except:
            db.desc = ""

        db.stock = opt

        try:
            db.sale = self.driver.find_element(By.CSS_SELECTOR,"#ProductDetails > div > div.ProductMain > div.ProductDetailsGrid > div.p-price > div.DetailRow.PriceRow > div > em.ProductPrice.VariationProductPrice.on-sale").text.encode("utf-8")
        except:
            db.sale = ""

        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
            db.min1 = self.driver.find_element(By.CSS_SELECTOR,"body > div.body > div.container > div > div.productView > section:nth-child(3) > div.productView-options > form > div.product-purchase-section > div.form-field.form-field--increments.show > div > input").get_attribute("value")
        except:
            db.min1 = 2
        
        if db.sale == "":
            db.price1 = 99
        else:
            db.price1 = 99

        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "JanMichael400"
        db.dir160 = "JanMichael160"

        self.time.sleep(1)

        try:
            db.img400 = self.driver.find_element(By.CSS_SELECTOR,"body > div.body > div.container > div > div.productView > section.productView-images > div > figure > div.productView-img-container > a > img").get_attribute("src").split("?")[0]
        except:
            try:
                db.img400 = self.driver.find_element(By.CSS_SELECTOR,"body > div.body > div.container > div > div.productView > section.productView-images > div > figure > div > a").get_attribute("href")
            except:
                print("Img not detected.")
                return

        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "JanMichael800"
        db.img800 = db.img160
        print(db)
        return db
        
    def search_item(self,row):
        print("\nSearching for item: " + row+"\n")
        self.driver.get("https://www.janmichaelsartandhome.com/search.php?search_query="+row+" ")
        self.time.sleep(1)
        # while True:
        #     try:
        #         try:
        #             WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#PopupSignupForm_0 > div.mc-modal > div.mc-closeModal"))).click()
        #         except:
        #             pass
        #         WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > header > div.navPages-section.navPages-section-1 > nav > ul > li > a"))).click()
        #         self.driver.find_element(By.CSS_SELECTOR,"#search_query").clear()
        #         self.driver.find_element(By.CSS_SELECTOR,"#search_query").send_keys(str(row+" "))
        #         self.time.sleep(2)
        #         break
        #     except:
        #         self.driver.get(self.home)
        #         self.time.sleep(1)
        #         continue

        try:
            # item = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"#search-preview-dropdown > div > section > ul > li > article > figure > a") if "http" in i.get_attribute("href")]
            item = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"#product-listing-container > div.product-view-mode > form > ul.productGrid.is-open > li > article > figure > a") if "http" in i.get_attribute("href")]
            #print type(item)
            #print item[0]
            #self.time.sleep(3)
            return [item[0]]
        except:
            return None

