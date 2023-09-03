import json
from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class seastones(domainobject.domainobject):

    vendor = "Sea Stones Products"
    url = "https://sea-stones.com/"
    login = "https://sea-stones.com/"
    home = "https://sea-stones.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville4"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.login)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("customer[email]").send_keys(un)
        # self.driver.find_element_by_name("customer[password]").send_keys(pw)
        # self.driver.find_element_by_name("customer[password]").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

  #This is used for click options if available then save info 
    def clickbtn(self,btn):
	
        opt = []
		
        for x in range(len(btn)):
        
            # while True:
                # try:
            b = self.driver.find_elements_by_css_selector("#productSelect-product-template-option-0 option")[x]
            if b.is_displayed():
                    # self.driver.find_elements_by_css_selector("select#product-variants-option-0 option")[x].click()
                b.click()
                print "Option selected."
                self.time.sleep(1)
                #     break
                # except Exception as e:
                #     print "Option click exception:"
                #     return
            self.time.sleep(1)
			# try:
				# optsize = self.driver.find_elements_by_css_selector("select#product-variants-option-1 option")
				# print "More sizes detected."
				# for o in optsize:
					# try:
						# o.click()
					# except Exception as a:
						# raise a
					# print "Size clicked."
					# self.time.sleep(1)
					# db = self.save_info()
					# print "\n"
					# opt.append(db)
            # except Exception as e:
                # print "Size click exception:" + e
            db = self.save_info()
            opt.append(db)

        return opt
        
		
		
		
    #Special for Janmichaels/Capitol_Imports in case options are available
    def get_info(self,item=None):
    
        option = []
        # WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.productOptionViewSelect > div > select option:nth-child(1)"))) #wait for option to load
        # btn = self.driver.find_elements_by_css_selector("div.productOptionViewSelect > div select:nth-child(1) option")
        try:
            btn = self.driver.find_elements_by_css_selector("#productSelect-product-template-option-0 option")
            print "Btn detected."
            db = self.clickbtn(btn)
            option.extend(db) #returns a list of items
        except Exception as e:
            print e
            print "Btn not found."
            db = self.save_info()
            option.append(db)
            
        return option
    
	
	
    def save_info(self,item=None):
        db = gateway()
        print "Getting item info."
        db.name = self.driver.find_element_by_css_selector("#ProductSection > div.grid > div.grid-item.large--two-fifths > h1").text.encode("utf-8")
        db.sku =  json.loads(json.dumps(self.driver.execute_script("return meta.product.variants;")[0]))["sku"]
        self.time.sleep(1)
        db.cat = ""
        try:
            db.desc = self.driver.find_element_by_css_selector("#ProductSection > div.product_tags.margin-bottom").text.encode("utf-8")
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
        db.dir400 = "Cap 400"
        db.dir160 = "Cap 160"
        db.img400 = self.driver.find_element_by_css_selector("#ProductSection > div > meta:nth-child(2)").get_attribute("content").split("?")[0]
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Cap 800"
        db.img800 = db.img160
        print db.retrieve()
        return db
        
        
    def search_item(self,row):
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                # self.driver.find_element_by_css_selector("#menu > li.search").click()
                # self.time.sleep(0.5)
                self.driver.find_element_by_name("q").clear()
                self.driver.find_element_by_name("q").send_keys(str(row))
                self.driver.find_element_by_name("q").send_keys(Keys.ENTER)
                self.time.sleep(self.delay)
                break
            except:
                self.driver.get(self.url)
                self.time.sleep(self.delay)
                continue

        try:
            item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#shopify-section-search-template > div > div > div > div > a")]
            print item
            return item
        except:
            return None

