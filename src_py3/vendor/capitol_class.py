import json
from helper import table_gateway 
from helper import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class capitol(domainobject.domainobject):

    vendor = "Capitol Imports"
    url = "https://www.earthrugs.com/"
    login = "https://www.earthrugs.com/account/login"
    home = "https://www.earthrugs.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville4"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.login)
        self.time.sleep(8)
        
        print("Logging in.")
        self.driver.find_element(By.NAME,"customer[email]").send_keys(un)
        self.driver.find_element(By.NAME,"customer[password]").send_keys(pw)
        self.driver.find_element(By.NAME,"customer[password]").send_keys(Keys.ENTER)
        while True:
            re = input("Enter yes when ready")
            if "yes" == re:
                break
            else:
                continue
        self.time.sleep(3)
        print("Success.")

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
                print("Option selected.")
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
    def g_info(self,item=None):
    
        option = []
        # WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.productOptionViewSelect > div > select option:nth-child(1)"))) #wait for option to load
        # btn = self.driver.find_elements_by_css_selector("div.productOptionViewSelect > div select:nth-child(1) option")
        try:
            btn = self.driver.find_elements_by_css_selector("#productSelect-product-template-option-0 option")
            print("Btn detected.")
            db = self.clickbtn(btn)
            option.extend(db) #returns a list of items
        except Exception as e:
            print(e)
            print("Btn not found.")
            db = self.save_info()
            option.append(db)
            
        return option
    
	
	
    def get_info(self,item=None):
        db = table_gateway.gateway()
        print("Getting item info.")
        db.name = self.driver.find_element_by_css_selector("#page-content > div.shopify-section.section-product-template > div > div.product-area__details.product-detail > div > div > div > h1").text.encode("utf-8")
        db.sku =  json.loads(json.dumps(self.driver.execute_script("return meta.product.variants;")[0]))["sku"]
        self.time.sleep(1)
        db.cat = ""
        try:
            db.desc = self.driver.find_element_by_css_selector("#page-content > div.shopify-section.section-product-template > div > div.product-area__details.product-detail > div > div > div > div.product-detail__tab-container.product-detail__gap-lg > div > div.cc-tabs__tab > div").text.encode("utf-8")
        except:
            db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = 1#self.driver.find_element_by_css_selector("#page-content > div.shopify-section.section-product-template > div > div.product-area__details.product-detail > div > div > div > form > div.product-detail__form__action.product-detail__gap-lg.product-detail__form__options--with-quantity > div > input").get_attribute("value")
        try:
            db.price1 = self.driver.find_element_by_css_selector("#page-content > div.shopify-section.section-product-template > div > div.product-area__details.product-detail > div > div > div > div.price-area.product-detail__gap-sm > span").text
        except:
            db.price1 = self.driver.find_element_by_css_selector("div.large--two-fifths:nth-child(4) > div:nth-child(2) > meta:nth-child(2)").get_attribute("content")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "Cap 400"
        db.dir160 = "Cap 160"
        try:
            db.img400 = self.driver.find_element_by_css_selector("#page-content > div.shopify-section.section-product-template > div > div.product-area__media.cc-animate-init.-in.cc-animate-complete > div > div > div.theme-images.swiper-wrapper > div > div > div > img").get_attribute("srcset").split(",")[3]
        except:
            db.img400 = self.driver.find_element_by_css_selector("#shopify-section-template--14551958356055__main > div > div.product-area__media.multi-column.cc-animate-init.-in.cc-animate-complete > div > div > div.theme-images.swiper-wrapper > div:nth-child(3) > div.theme-img.theme-img-4.swiper-slide > div > div > img").get_attribute("srcset").split(",")[3]
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Cap 800"
        db.img800 = db.img160
        print(db)
        return db
        
        
    def search_item(self,row):
        print("\nSearching for item: " + row+"\n")
        while True:
            try:
                self.driver.find_element_by_css_selector("#site-control > div.links.site-control__inner > div.nav-right-side > a.cart.nav-search").click()
                self.time.sleep(0.5)
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
            item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#page-content > div > div > div.cc-animate-init.-in.cc-animate-complete > div > div.product-list-container.product-list-container--with-sidebar > div > div > div > div.image > a")]
            print(item)
            return(item)
        except:
            return None

