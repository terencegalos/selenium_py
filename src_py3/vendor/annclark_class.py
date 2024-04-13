from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class annclark(domainobject):

    def __init__(self,driver,mode):
        super().__init__(driver)
        self.mode = mode
        self.links = []


    vendor = "Ann Clark Cookie Cutters"
    url = "https://wholesale.annclarkcookiecutters.com/"
    home = "https://wholesale.annclarkcookiecutters.com/"
    uname = "sherie@waresitat.com"
    passw = "sherie020123"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(3)
        
        print("Logging in.")
        self.driver.find_element(By.NAME,"username").send_keys(un)
        self.driver.find_element(By.NAME,"password").send_keys(pw)
        self.driver.find_element(By.NAME,"password").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print("Success.")

    def get_info(self,item=None):
        db = gateway()
        print("Acquiring product info.")
        db.name = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#content > form > section > div.info.iefix > div.content > h1"))).text
        try:
            db.sku = self.driver.find_element(By.CSS_SELECTOR,"div.sku").text
        except:
            db.sku = ""
        db.cat = "|".join([i.text for i in self.driver.find_elements(By.CSS_SELECTOR,"#breadcrumb > ol > li")])
        try:
            db.desc = self.driver.find_element(By.CSS_SELECTOR,"#product_desc").text
        except:
            db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = ""
        db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "AnnClark400"
        db.dir160 = "AnnClark160"
        # db.img400 = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a.MagicZoom"))).get_attribute("href")
        db.img400 = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#content > form > section > div.image.iefix > a > img"))).get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "AnnClark800"
        db.img800 = db.img160
        print("Printing product info.")
        print(db)
        return db
        
        
    def search_item(self,row):
        
        print("\nSearching for item: " + row+"\n")
        
        # self.driver.find_element(By.CSS_SELECTOR,"#nav-search-btn").click()
        # self.time.sleep(1.5)
        # ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#search #search_keyword")).perform()
        # self.time.sleep(2)
        # print self.driver.find_element(By.CSS_SELECTOR,"#search").get_attribute("innerHTML")
        # self.time.sleep(2)
        # self.driver.find_element(By.CSS_SELECTOR,"#search #search_keyword").clear()
        # self.driver.find_element(By.CSS_SELECTOR,"#search_keyword").send_keys(row.rstrip())
        # self.driver.find_element(By.CSS_SELECTOR,"#search_keyword").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        self.driver.get("https://wholesale.annclarkcookiecutters.com/category/s?keyword="+row.rstrip())
        self.time.sleep(1)

        
        try:
            try:
                item = self.driver.find_element(By.CSS_SELECTOR,"div.content a").get_attribute("href")
            except:
                item = self.driver.find_element(By.CSS_SELECTOR,"#content_only > section > div > a").get_attribute("href")
            if item == "https://www.annclarkcookiecutters.com/product/custom-pillsbury-doughboy-cookie-cutter/food-services":
                return None
            return [item]
        except:
            return None


