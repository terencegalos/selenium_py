from table_gateway import gateway
import domainobject
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class cmpottery(domainobject.domainobject):

    vendor = "Cedar Mesa Pottery"
    url = "https://www.cmpotterywholesale.com/"
    home = "https://www.cmpotterywholesale.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in." 
        # self.driver.find_element_by_name("email").send_keys(un)
        # self.driver.find_element_by_name("password").send_keys(pw)
        # self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
		db = gateway()
		db.name = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#detail_parent_prod_nm"))).text.encode("utf-8")
		db.sku = self.driver.find_element_by_css_selector("#detail_info_sku > span:nth-child(2)").text.encode("utf-8")
		db.cat = self.driver.find_element_by_css_selector("#detail_info_type").text.encode("utf-8")
		try:
			db.desc = self.driver.find_element_by_css_selector("#detail_desc_content_1").text.encode("utf-8")
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
		db.dir400 = "cedarmesa400"
		db.dir160 = "cedarmesa160"
		db.img400 = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#detail_large"))).get_attribute("href")
		db.img160 = db.img400.split("/")[-1:][0]
		db.desc2 = ""
		db.option = ""
		db.dir800 = "cedarmesa800"
		db.img800 = db.img160     
		print db
		return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        
        while True:
			try:
				self.driver.find_element_by_name("u_search_text").clear()
				self.driver.find_element_by_name("u_search_text").send_keys(row.rstrip())
				self.driver.find_element_by_name("u_search_text").send_keys(Keys.ENTER)
				self.time.sleep(1)
				break
			except:
				self.driver.refresh()
				self.time.sleep(1)
				continue

        
        try:
            item = self.driver.find_element_by_css_selector("td.product_desc > p > strong > a").get_attribute("href")
            return [item]
        except:
            return None


