from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class janmichaelsale(domainobject.domainobject):

    vendor = "JanMichael's Home Closeout Sale"
    url = "https://www.janmichaelsartandhome.com/"
    home = "https://www.janmichaelsartandhome.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    links = []
    
        
    def nextPage(self):
        try:
            self.driver.find_element_by_css_selector("#product-listing-container > div > ul > li.pagination-item.pagination-item--next > a").click()
            self.time.sleep(1)
            return True
        except:
            print "Page exhausted."
            return False

    def get_links(self):
        ln = [l.get_attribute("href") for l in self.driver.find_elements_by_css_selector("#product-listing-container > form:nth-child(2) > div > div > div > article > div > h4 > a") if l.get_attribute("href") not in self.links] # will get return emtpy if already
        print ln
        return ln

    def get_all_items(self):
        self.driver.get("https://www.janmichaelsartandhome.com/sitemap/categories/")
        self.time.sleep(1)
        cats = [cat.get_attribute("href") for cat in self.driver.find_elements_by_css_selector("body > div.body > main > div > ul li a")]# if "clearance" not in cat.get_attribute("href")]
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
        
        print "Logging in."
        self.driver.find_element_by_id("login_email").send_keys(un)
        self.driver.find_element_by_id("login_pass").send_keys(pw)
        self.driver.find_element_by_id("login_pass").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."
    
    #This is used for click options if available then save info 
    def clickbtn(self,btn):
        opt = []
        optcount = len(btn.find_elements_by_css_selector("option"))

        for x in range(1,optcount):
            btn = self.driver.find_element_by_css_selector("select.form-select:nth-child(2)")
            try:
                btn.find_elements_by_css_selector("option")[x].click()
                db = self.save_info(btn.find_elements_by_css_selector("option")[x].text if "Frame" in btn.find_elements_by_css_selector("option")[x].get_attribute("innerHTML") else "")
                self.time.sleep(1)
                print "Option selected."
                opt.append(db)
            except:
                continue

        return opt
        
    #Special for Janmichaels in case options are available
    def get_info(self,item=None):
    
        option = []
        try:
            btn = self.driver.find_element_by_css_selector("select.form-select:nth-child(2)")
            print "Btn detected."
            db = self.clickbtn(btn)
            option.extend(db) #returns a list of items
        except:
            print "Btn not found."
            db = self.save_info()
            option.append(db)
            
        return option
    
    def save_info(self,opt=""):
        db = gateway()

        db.name = self.driver.find_element_by_css_selector("h1").text.encode("utf-8")

        try:
            db.sku = WebDriverWait(self.driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div.body > div:nth-child(2) > div:nth-child(1) > div > div.productView-top > section:nth-child(1) > div > dl > dd:nth-child(2)"))).text.encode("utf-8")
        except:
            print "No sku detected. Stopping."
            return
        
        db.cat = opt

        try:
            db.desc = self.driver.find_element_by_css_selector("#tab-description > p").text.encode("utf-8")
        except:
            db.desc = ""

        db.stock = ""

        try:
            db.sale = self.driver.find_element_by_css_selector("#ProductDetails > div > div.ProductMain > div.ProductDetailsGrid > div.p-price > div.DetailRow.PriceRow > div > em.ProductPrice.VariationProductPrice.on-sale").text.encode("utf-8")
        except:
            db.sale = ""

        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = self.driver.find_element_by_css_selector("body > div.body > div:nth-child(2) > div:nth-child(1) > div > div.productView-top > section:nth-child(3) > div.productView-options > form > div.form-field.form-field--increments > div > input").get_attribute("value")
        
        if db.sale == "":
            db.price1 = ""
        else:
            db.price1 = ""

        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "JanMichael400"
        db.dir160 = "JanMichael160"

        try:
			ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("a.productView-thumbnail-link")).perform()
        except:
			return

        self.time.sleep(1)

        try:
			db.img400 = self.driver.find_element_by_css_selector("body > div.body > div:nth-child(2) > div:nth-child(1) > div > div.productView-top > section.productView-images > figure > a > img").get_attribute("src").split("?")[0]
        except:
			print "Img not detected."
			return

        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "JanMichael800"
        db.img800 = db.img160
        print db
        return db
        
    def search_item(self,row):
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                try:
                    WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#PopupSignupForm_0 > div.mc-modal > div.mc-closeModal"))).click()
                except:
                    pass
                WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > header > div.navPages-section.navPages-section-1 > nav > ul > li > a"))).click()
                self.driver.find_element_by_name("search_query").clear()
                self.driver.find_element_by_name("search_query").send_keys(str(row+" "))
                self.time.sleep(2)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        try:
            item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#search-preview-dropdown > div > section > ul > li > article > figure > a") if "http" in i.get_attribute("href")]
            #print type(item)
            #print item[0]
            #self.time.sleep(3)
            return [item[0]]
        except:
            return None

