from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class carsonflags(domainobject.domainobject):
    vendor = "Carson Home - Flags"
    url = "https://www.carsonhomeaccents.com/security_logon.asp?autopage=%2Fdefault%2Easp"
    home = "https://www.carsonhomeaccents.com/"
    uname = "rstuart"
    passw = "Wolfville4"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        print "Logging in..."
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "logonUsername"))).send_keys(un)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "logonPassword"))).send_keys(pw)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "logonPassword"))).send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
		while True:
			try:
			
				dbs = []
				opt = self.driver.find_elements_by_css_selector("#prod_opt1 > option")
				
				try:
					self.driver.find_elements_by_css_selector("#prod_opt1 > option")[0].click()
					print "Option detected."
				except:
					raise
				
				for o in range(len(opt)):
					self.driver.find_elements_by_css_selector("#prod_opt1 > option")[o].click()
					self.time.sleep(1)
					db = self.save_info()
					
					try:
						opt2 = self.driver.find_elements_by_css_selector("#prod_opt2 > option")
						for o2 in range(len(o2)):
							self.driver.find_elements_by_css_selector("#prod_opt2 > option")[o2].click()
							self.time.sleep(1)
							db = self.save_info()
					except:
						db = self.save_info()
					
					dbs.append(db)
					
				return dbs
				
			except:
				print "No option."
				db = self.save_info()
				print db
				return db
			
    def save_info(self,item=None):
		try:
			db = gateway()
			
			try:
				db.name = self.driver.find_element_by_css_selector("#detail_parent_prod_nm").text.encode("utf-8")
				
			except:
				self.driver.refresh()
				self.time.sleep(1)
				db.name = self.driver.find_element_by_css_selector("#detail_parent_prod_nm").text.encode("utf-8")
				
			try:
				try:
					db.sku = self.driver.find_element_by_css_selector("#sku_container").text.encode("utf-8").split()[1]
				except:
					db.sku = self.driver.find_element_by_css_selector("span[itemprop=sku]").text.encode("utf-8")
			except:
				db.sku = item
				
			db.cat = ""

			try:
				db.desc = self.driver.find_element_by_css_selector(".detail_desc_content").text.encode("utf-8")
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
			db.dir400 = "Carson400"
			db.dir160 = "Carson160"
			self.time.sleep(1)
			#db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#fancybox-img"))).get_attribute("src")
			db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#detail_enlarge"))).get_attribute("href")
			db.img160 = db.img400.split("/")[-1:][0]

			try:
				db.desc2 = self.driver.find_element_by_css_selector("#detail_info_brand").text.encode("utf-8")
			except:
				db.desc2 = ""

			db.option = "|".join(i.text.encode("utf-8").strip() for i in self.driver.find_elements_by_tag_name("option"))
			db.dir800 = "Carson800"
			db.img800 = db.img160
			print db
			return db
		except:
			return None
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("search_keyword").clear()
                self.driver.find_element_by_name("search_keyword").send_keys(row)
                self.driver.find_element_by_name("search_keyword").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                continue
        try:
            item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("div.item_row.nm a")]
            print item
            return item
        except:
            return None
