from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import xml.etree.ElementTree as tree

class packagingsourcet(domainobject.domainobject):

    vendor = "The Packaging Source"
    url = "http://www.packagingsource.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    #xml sitemap for this vendor
    tree = tree.parse("./csv/infile/sitemap.xml")
    links = [node.text for node in tree.iter() if node.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"]
    links = [link for link in links if "www.packagingsource.com/store/c" not in link]
    # print len(links)
    
        
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
    def clickbtn(self,btn,option=None):
        opt = []
        # print optcount
        for x in range(1,len(btn),opt):
            print self.driver.find_elements_by_css_selector("option")[x].get_attribute("innerHTML")
            self.driver.find_elements_by_css_selector("option")[x].click()
            print "Option selected."
            self.time.sleep(1)
            db = self.save_info(None,option)
            print "\n"
            opt.append(db)
        return opt
        
    #Special for Janmichaels in case options are available
    def get_info(self,item=None):
    
        varitems = []
        # WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"option"))) #wait for option to load
        btn = self.driver.find_elements_by_tag_name("select")
        print len(btn)
        
        if len(btn) > 0:
			option = ""			
			#make option if available
			for x in range(len(btn)):
				# print (self.driver.execute_script("return document.querySelectorAll('select')["+str(x)+"].parentNode")).find_element_by_css_selector("div").text
				if "color" in (self.driver.execute_script("return document.querySelectorAll('select')["+str(x)+"].parentNode")).find_element_by_css_selector("div").text.lower():
					opt = self.driver.execute_script("return document.querySelectorAll('select')["+str(x)+"]")
					option += "||"+"|".join([o.text for o in opt.find_elements_by_css_selector("option")])
					print "Btn detected."
			
			# print option
			
			#navigate options to update price
			for x in range(len(btn)):
				if "color" not in (self.driver.execute_script("return document.querySelectorAll('select')["+str(x)+"].parentNode")).find_element_by_css_selector("div").text.lower():
					db = self.clickbtn(btn[x],option)
					option.extend(db) #returns a list of items
					print "Price variety detected."
				else:
					print "Getting info for select: "+repr(x)
					db = self.save_info(None,option)
					varitems.append(db)
					
        else:
            print "No option found. Saving info..."
            db = self.save_info(None,option)
            varitems.append(db)
            
        return varitems
    
    
	
	
    def save_info(self,item=None,option=None):
        db = gateway()
        try:
            # db.name = self.driver.find_element_by_css_selector("h1.ProductDetailsProductName.no-m-t").text.encode("utf-8")
            db.name = self.driver.find_element_by_css_selector("div.page-header.no-m-t > div").text.encode("utf-8")
        except:
            return
        if item is None:
            db.sku = WebDriverWait(self.driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#lblItemNr"))).text.encode("utf-8")
        else:
            db.sku = WebDriverWait(self.driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#lblItemNr"))).text.encode("utf-8")+"|"+item
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
			db.img400 = self.driver.find_element_by_css_selector("a.main-product-photo.block.zoom.rel").get_attribute("href").split("?")[0]
        except:
			print "Img not detected."
			return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = option
        db.dir800 = "Packaging400"
        db.img800 = db.img160
        print db
        return db
        
    def search_item(self,row):
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_css_selector("div > div.navbar-collapse.collapse > div > ul > li:nth-child(1) > a > i").click()
                self.time.sleep(1)
                self.driver.find_element_by_name("txtRedirectSearchBox").clear()
                self.driver.find_element_by_name("txtRedirectSearchBox").send_keys(row.split()[0])
                self.driver.find_element_by_name("txtRedirectSearchBox").send_keys(Keys.ENTER)
                self.time.sleep(2)
                break
            except:
                self.driver.get(self.url)
                self.time.sleep(1)
                continue

        try:
            item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#MainForm > div.Layout.container > section > section > div.LayoutContentInner > div.product-list > div > div > div > div.no-m-b > a")]
            return item
        except:
            return None

