from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import xml.etree.ElementTree as tree
import requests,xmltodict

class packagingsource(domainobject.domainobject):

    vendor = "The Packaging Source"
    url = "http://www.packagingsource.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    links = []
    flag = False
    lastStop = "http://www.packagingsource.com/glitter-unicorn-gourmet-window-boxes.html"
    # xml sitemap for this vendor

    # xmlfile = requests.get("http://www.packagingsource.com/sitemap.xml")
    # tree = tree.parse("./csv/infile/sitemap.xml")
    # links = [node.text for node in tree.iter() if node.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"]
    # links = [link for link in links if "/store/c/" not in link]
    
        
    def read_sitemap(self):
        xmlfile = requests.get("https://www.packagingsource.com/sitemap.xml")
        self.time.sleep(1)
        data = xmltodict.parse(xmlfile.content)
        print data
        self.links.extend([link['loc'] for link in data['urlset']['url'] if "/store/c/" not in link['loc']])


    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element_by_css_selector("div > div.navbar-collapse.collapse > ul > li:nth-child(6) > a").click()
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("txtEmailAddress").send_keys(un)
        self.driver.find_element_by_name("txtPassword").send_keys(pw)
        self.driver.find_element_by_name("btnSignIn").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."
    
    #This is used for click options if available then save info
    def clickbtn(self,btn):
        optstore = []
        optcount = len(btn)
        print optcount
        for x in range(0,optcount):
            currentBtn = self.driver.find_elements_by_tag_name("select")[x]
            opt = currentBtn.find_elements_by_css_selector("option")
            for o in range(1,len(opt)):
                print currentBtn.find_elements_by_css_selector("option")[o].get_attribute("innerHTML")
                currentBtn.find_elements_by_css_selector("option")[o].click()
                print "Option selected."
                self.time.sleep(1)
                print currentBtn.find_elements_by_css_selector("option")[o].text.encode("utf-8")
                db = self.save_info(currentBtn.find_elements_by_css_selector("option")[o].text.encode("utf-8"))
                print "\n"
                optstore.append(db)
        return optstore
        
    #Special for Janmichaels in case options are available
    def get_info(self,item=None):
    
        option = []
        # WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"option"))) #wait for option to load
        btn = self.driver.find_elements_by_css_selector("select[name*=Variant]")
        if len(btn) > 0: # check option if available
            if "$" in btn[0].get_attribute("innerHTML"):
                print "Btn detected."
                db = self.clickbtn(btn)
                option.extend(db) #returns a list of items
            else:
                db = self.save_info()
                option.append(db)
        else:
            print "No option with pricing found. Saving info immediately..."
            db = self.save_info()
            option.append(db)
            
        return option
    
    def save_info(self,item=None):
        db = gateway()
        try:
            # db.name = self.driver.find_element_by_css_selector("h1.ProductDetailsProductName.no-m-t").text.encode("utf-8")
            db.name = self.driver.find_element_by_css_selector("div.page-header.no-m-t > div").text.encode("utf-8")
            print db.name
        except:
            print "Not an item. Skipping."
            return
        try:
            db.sku = WebDriverWait(self.driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#lblItemNr"))).text.encode("utf-8")
        except:
            try:
                db.sku = WebDriverWait(self.driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#lblItemNr"))).text.encode("utf-8")+" - "+item
            except:
                db.sku = db.name

        db.cat = "|".join([c.text.encode("utf-8") for c in self.driver.find_elements_by_css_selector("#lblCategoryTrail a")])
        try:
			db.desc = self.driver.find_element_by_css_selector("#desc1").text.encode("utf-8")
        except:
			db.desc = ""
        db.stock = ""
        try:
            db.sale = self.driver.find_element_by_css_selector("#ProductDetails > div > div.ProductMain > div.ProductDetailsGrid > div.p-price > div.DetailRow.PriceRow > div > em.ProductPrice.VariationProductPrice.on-sale").text.encode("utf-8")
        except:
            db.sale = ""
        try:
            db.set = self.driver.find_element_by_xpath("//*[@id=\"MainForm\"]/div[2]/section/section/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div/text()").text.encode("utf-8")
        except:
            db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
            db.min1 = self.driver.find_element_by_css_selector("#txtQuantity").get_attribute("value")
        except:
            db.min1 = "sold out?"
        try:
            db.price1 = self.driver.find_element_by_css_selector("#lblPrice").text.encode("utf-8")
        except:
            db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "Packaging400"
        db.dir160 = "Packaging160"
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#TinyImage_0")).perform()
        # self.time.sleep(1)
        try:
			db.img400 = self.driver.find_element_by_css_selector("a.main-product-photo.block.zoom.rel").get_attribute("href")
        except:
			print "Img not detected."
			return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        try:
            dropdown = self.driver.find_elements_by_tag_name("select")
            for drop in dropdown:
                choice = [ch.text for ch in drop.find_elements_by_css_selector("option")]
                db.option = "|".join(choice)
        except:
            db.option = ""
            
        db.dir800 = "Packaging400"
        db.img800 = db.img160
        print db
        return db
        
    def search_item(self,row):
        print "\nSearching for item: " + row+"\n"
        # self.driver.find_element_by_css_selector("div > div.navbar-collapse.collapse > div > ul > li:nth-child(1) > a > i").click()
        while True:
            print "Search attempt..."
            try:
                self.driver.find_element_by_css_selector("div > div.navbar-collapse.collapse > div > ul > li:nth-child(1) > a").click()
                self.time.sleep(1)
                self.driver.find_element_by_name("txtRedirectSearchBox").clear()
                self.driver.find_element_by_name("txtRedirectSearchBox").send_keys(row)
                self.driver.find_element_by_name("txtRedirectSearchBox").send_keys(Keys.ENTER)
                self.time.sleep(2)
                break
            except:
                self.driver.get(self.url)
                self.time.sleep(1)
                continue

        try:
            item = [i.get_attribute("href") for i in self.driver.find_element_by_css_selector("#MainForm > div.Layout.container > section > section > div.LayoutContentInner > div.product-list > div > div > div > div.no-m-b > a")]
            return item
        except:
            return None

