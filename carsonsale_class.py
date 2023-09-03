from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class carsonsale(domainobject.domainobject):
    vendor = "Carson Home Accents 50% Off"
    url = "https://www.carsonhomeaccents.com/security_logon.asp?autopage=%2Fdefault%2Easp"
    home = "https://www.carsonhomeaccents.com/"
    uname = "rstuart"
    passw = "Wolfville4"
    delay = 1
    links = []
    lastStop = "http://www.carsonhomeaccents.com/pc_product_detail.asp?key=99654C631C1E4C43BCA179128FFB9CB6&catid="
    flag = False
    
    def nextPage(self):
		try:
			self.driver.find_elements_by_css_selector("a.xresults_pagenext")[-1].click()
			return True
		except:
			print "Page exhausted."
			return False

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#sw_dropdown_778 > a")).perform()
        # self.time.sleep(1)
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
				
				try: #check if clickable or raise error
					self.driver.find_elements_by_css_selector("#prod_opt1 > option")[0].click()
					print "Option detected."
				except:
					raise
				
				for o in range(len(opt)): #loop every option
					self.driver.find_elements_by_css_selector("#prod_opt1 > option")[o].click()
					self.time.sleep(1)
					db = self.save_info()
					
					try: #loop option two if available
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
		try:
			db.sale = self.driver.find_element_by_css_selector("li.saleprice").text.encode("utf-8")
		except:
			return None
			
		db.set = ""
		db.custom = ""
		db.size = ""
		db.seller = ""
		db.min1 = self.driver.find_element_by_css_selector("#qty_box").get_attribute("value")
		try:
			db.price1 = self.driver.find_element_by_css_selector("#frmAddToCart > div.detail_cart > ul.detail_pricing > li.listprice > span").text.encode("utf-8")
		except:
			db.price1 = self.driver.find_element_by_css_selector("li.saleprice").text.encode("utf-8")
			db.sale = ""
		db.min2 = ""
		db.price2 = ""
		db.min3 = ""
		db.price3 = ""
		db.multi = db.min1
		db.dir400 = "Carson400"
		db.dir160 = "Carson160"
		self.time.sleep(1)
		db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#detail_enlarge"))).get_attribute("href")
		db.img160 = db.img400.split("/")[-1:][0]

		try:
			db.desc2 = self.driver.find_element_by_css_selector("#detail_info_brand").text.encode("utf-8")
		except:
			db.desc2 = ""

		try:
			db.option = "|".join(i.text.encode("utf-8").strip() for i in self.driver.find_elements_by_tag_name("option"))
		except:
			db.option = ""

		db.dir800 = "Carson800"
		db.img800 = db.img160

		print db
		return db
        
        
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
            self.driver.find_element_by_css_selector("#rpp1 > option:nth-child(5)").click() #show 120 items
            self.time.sleep(1)
            self.links = [] # empty links before adding
            item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("div.item_row.nm a") if i.get_attribute("href") not in self.links]
            print item
            self.links.extend([item[0]])
            # while self.nextPage():
			# 	item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("div.item_row.nm a") if i.get_attribute("href") not in self.links]
			# 	print item
			# 	self.links.extend(item)

            return self.links

        except:
            return None