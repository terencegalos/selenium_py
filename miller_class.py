from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class miller(domainobject.domainobject):
    vendor = "Miller Decor"
    url = "http://www.millerdecor.com/page/password/8985573.htm"
    home = "http://www.millerdecor.com/index.html"
    uname = "rick@waresitat.com"
    passw = "Inspire2day"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#sw_dropdown_778 > a")).perform()
        # self.time.sleep(1)
        print "Logging in..."
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "logonUsername"))).send_keys(un)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(pw)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
		dbs = []
		opt = self.driver.find_elements_by_css_selector("select#variantSelect option")
		if len(opt) > 0:
			for c in range(len(opt)):
				self.driver.find_elements_by_css_selector("select#variantSelect option")[c].click()
				self.time.sleep(1)
				db = self.save_info(item)
				print db
				dbs.append(db)

			return dbs
		else:
			db = self.save_info(item)
			print db
			return db
			
			
    def save_info(self,item=None):
		db = gateway()
		try:
			db.name = self.driver.find_element_by_css_selector("#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > font:nth-child(2) > strong > div").text.encode("utf-8")
		except:
			self.driver.refresh()
			self.time.sleep(1)
			db.name = ""
		try:
			db.sku = self.driver.find_element_by_css_selector("#code").text.encode("utf-8")
		except:
			db.sku = item
		db.cat = self.driver.find_element_by_css_selector("#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > font:nth-child(1) > a").text.encode("utf-8")
		db.desc = ""
		try:
			db.stock = self.driver.find_element_by_css_selector("#availability").text.encode("utf-8")
		except:
			db.stock = ""
		db.sale = ""
		db.set = ""
		db.custom = ""
		db.size = item
		db.seller = ""
		db.min1 = ""
		try:
			db.price1 = self.driver.find_element_by_css_selector("#price > strong").text.encode("utf-8")
		except:
			db.price1 = ""
		db.min2 = ""
		db.price2 = ""
		db.min3 = ""
		db.price3 = ""
		db.multi = ""
		db.dir400 = "Millers400"
		db.dir160 = "Millers160"
		self.time.sleep(1)
		try:
			db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > div > p > img"))).get_attribute("src")
		except:
			db.img400 = ""
		# db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > div > p:nth-child(11) > img"))).get_attribute("src")
		db.img160 = db.img400.split("/")[-1:][0]
		db.desc2 = ""
		db.option = "|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("select[name='option_1'] option")])
		db.dir800 = "Millers800"
		db.img800 = db.img160
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
            item = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("div.item_row.nm a")]
            return item
        except:
            return None
