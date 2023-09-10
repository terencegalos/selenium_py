from selenium.webdriver.common.keys import Keys
from table_gateway import gateway
import domainobject
from selenium.webdriver.common.action_chains import ActionChains

class gooseberry(domainobject.domainobject):

    vendor = "Gooseberry Patch Cookbooks"
    url = "https://www.gooseberrypatch.com/gooseberry/recipe.nsf/f.onlinerecipebox"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    login = "https://www.gooseberrypatch.com/gooseberry/recipe.nsf/f.onlinerecipebox"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(5)
        
        # print "Logging in."
        # self.driver.find_element_by_name("LOG_ID").send_keys(un)
        # self.driver.find_element_by_name("LOG_ID").send_keys(Keys.TAB)
        # self.driver.find_element_by_name("LOG_ID").click()
        # self.time.sleep(1)
        # self.driver.find_element_by_id("password").send_keys(pw)
        # self.driver.find_element_by_id("password").send_keys(Keys.ENTER)
        # self.time.sleep(3)
        # print "Success."

    def get_info(self,item=None):
		db = gateway()
		db.name = self.driver.find_element_by_css_selector("body > form > div.mainContainer > table:nth-child(7) > tbody > tr:nth-child(2) > td > table:nth-child(6) > tbody > tr > td > table:nth-child(2) > tbody > tr > td:nth-child(3) > font:nth-child(1) > strong").text.encode("utf-8")
		db.sku = item
		db.cat = "|".join([l.text.encode("utf-8") for l in self.driver.find_elements_by_css_selector("body > form > div.mainContainer > table:nth-child(7) > tbody > tr:nth-child(2) > td > table:nth-child(6) > tbody > tr > td > table:nth-child(1) > tbody > tr > td > b > a")])
		db.desc = ""
		db.stock = ""
		db.sale = ""
		db.set = ""
		db.custom = ""
		db.size = ""
		db.seller = ""
		db.min1 = 1
		db.price1 = 99
		db.min2 = ""
		db.price2 = ""
		db.min3 = ""
		db.price3 = ""
		db.multi = 1
		db.dir400 = "Gooseberry400"
		db.dir160 = "Gooseberry160"
		try:
			db.img400 = self.driver.find_element_by_css_selector("#main").get_attribute("src")
		except:
			print "Image not found."
			return
		db.img160 = db.img400.split("/")[-1:][0]
		db.desc2 = ""
		db.option = ""
		db.dir800 = "Gooseberry800"
		db.img800 = db.img160
		print db
		return db
        
        
    def search_item(self,row):

		print "\nSearching for item: " + row[1:]+"\n"
		self.time.sleep(2)
		self.driver.find_element_by_name("globalkeyword").clear()			
		self.driver.find_element_by_name("globalkeyword").send_keys(str(row[1:]))
		self.time.sleep(1)
		self.driver.find_element_by_css_selector("img[title='Click here to Search']").click()
		self.time.sleep(1)
		
		try:
			# self.driver.find_element_by_css_selector("#results > table > tbody > tr:nth-child(2) > td > p > a:nth-child(1)").click()
			self.driver.find_element_by_css_selector("#results > table > tbody > tr:nth-child(2) > td > p > b > a").click()
			self.time.sleep(1)
		except:
			return None

