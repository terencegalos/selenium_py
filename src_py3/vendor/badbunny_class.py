import json
import random
from helper import table_gateway 
from helper import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


class badbunny(domainobject.domainobject):

    def __init__(self,driver,scraper_mode):
        super().__init__(driver)
        self.mode = scraper_mode

    vendor = "Bad Bunny"
    url = "https://badbunnydesigns.com/"
    login = "https://badbunnydesigns.com/m/login?r=%2Fm%2Faccount"
    uname = "service@waresitat.com"
    passw = "wolfville"
    delay = 1
    links = []
    all_product_urls = []
    lastStop = 'https://badbunnydesigns.com/shop/ols/products/day-drink-and-work-in-my-garden-cork-back-drink-coasters-set-of-4-4-x-4in'
    
    # paginate up to page 18; start page 1
    pagenum = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.login)
        self.time.sleep(1)
        
        print("Logging in.")
        self.driver.find_element(By.NAME,"email").send_keys(un)
        self.driver.find_element(By.NAME,"password").send_keys(pw)
        self.driver.find_element(By.NAME,"password").send_keys(Keys.ENTER)
        self.time.sleep(2)
        print("Success.")
        
    def paginate(self):
        try:
            # next = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div/div/span/div/section/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/div/a[2]')
            # self.driver.get(next.get_attribute('href').replace("-",""))
            if self.pagenum > 18:
                raise 'Exiting pagination'
            self.driver.get(f"https://badbunnydesigns.com/shop/ols/products?page={self.pagenum}")
            print('Next page..')
            self.time.sleep(3)
            self.pagenum += 1
            return True
        except NoSuchElementException:
            print('Exiting pagination.')
            return False
        except TypeError:
            print('Exiting pagination.')
            return False

  #This is used for clicking options if available then save info 
    def clickbtn(self,btn):
	
        opt = []
		
        for x in range(len(btn)):
        
            # while True:
                # try:
            b = self.driver.find_elements(By.CSS_SELECTOR,"#productSelect-product-template-option-0 option")[x]
            if b.is_displayed():
                    # self.driver.find_elements(By.CSS_SELECTOR,"select#product-variants-option-0 option")[x].click()
                b.click()
                print("Option selected.")
                self.time.sleep(1)
                #     break
                # except Exception as e:
                #     print "Option click exception:"
                #     return
            self.time.sleep(1)
			# try:
				# optsize = self.driver.find_elements(By.CSS_SELECTOR,"select#product-variants-option-1 option")
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
        # btn = self.driver.find_elements(By.CSS_SELECTOR,"div.productOptionViewSelect > div select:nth-child(1) option")
        try:
            btn = self.driver.find_elements(By.CSS_SELECTOR,"#productSelect-product-template-option-0 option")
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
        
        print(f"Getting item info: {self.driver.current_url}")
        try:
            WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div/div/span/div/section/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div/h1')))
            db.name = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/span/div/section/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div/h1").text
        except NoSuchElementException:
            self.driver.refresh()
            self.time.sleep(1)
            WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div/div/span/div/section/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div/h1')))
            db.name = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/span/div/section/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div/h1").text
        db.sku =  db.name
        db.cat = ""
        db.desc = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/span/div/section/div/div/div[2]/div/div/div[1]/div[2]/div/div[3]").text
        db.stock = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/span/div/section/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/input").get_attribute("value")
        db.price1 = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/span/div/section/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div/div/div").text
        db.sale = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "badbunny400"
        db.dir160 = "badbunny160"
        
        img = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div/div/span/div/section/div/div/div[2]/div/div/div[1]/div[1]')
        ActionChains(self.driver).move_to_element(img).pause(0.5).perform()
        try:
            WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="ols-image-wrapper"]/div/img')))
            db.img400 = self.driver.find_element(By.CSS_SELECTOR,"#ols-image-wrapper img").get_attribute("src")
        except NoSuchElementException:
            db.img400 = self.driver.find_element(By.XPATH,'//*[@id="ols-image-wrapper"]/div/div/img').get_attribute("src")
        except TimeoutException:
            try:
                self.driver.refresh()
                self.time.sleep(1)
                WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="ols-image-wrapper"]/div/img')))
                db.img400 = self.driver.find_element(By.XPATH,'//*[@id="ols-image-wrapper"]/div/img').get_attribute("src")
            except TimeoutException:
                self.driver.refresh()
                self.time.sleep(1)
                WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="ols-image-wrapper"]/img')))
                db.img400 = self.driver.find_element(By.XPATH,'//*[@id="ols-image-wrapper"]/img').get_attribute("src")
                
            
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "badbunny800"
        db.img800 = db.img160
        print(db)
        return db
        
        
    def search_item(self,row):
        print("\nSearching for item: " + row+"\n")
        # self.driver.get(f"https://badbunnydesigns.com/shop/ols/products?page=1")
        self.driver.get(f"https://badbunnydesigns.com/shop/ols/search?keywords={row}&sortOption=descend_by_match")
        self.time.sleep(3)
        

        
        def scrape_product_urls():
            print('Extracting product urls.')
            items = []
            try:
                # WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/span/div/section/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/a")))
                # items_selectors = self.driver.find_elements(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div/div/span/div/section/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/a")
                items_selectors = self.driver.find_elements(By.XPATH,'//*[@id="bs-9"]/span/div/section/div/div/div[3]/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a')
                for selector in items_selectors: # return first result
                    item = selector.get_attribute("href")
                    print(f"Result: {item}")
                    items.append(item)
            except TimeoutException:
                print("Search returns no result.")
            return items
            
        self.all_product_urls.extend(scrape_product_urls())
        # while self.paginate():
        #     self.all_product_urls.extend(scrape_product_urls())
            
        return set(self.all_product_urls)
            

