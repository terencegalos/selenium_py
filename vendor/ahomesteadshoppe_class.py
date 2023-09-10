from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ahomesteadshoppe(domainobject.domainobject):

    vendor = "A_Homestead_Shoppe"
    url = "http://www.ahomesteadshoppe.com/"
    home = "http://www.ahomesteadshoppe.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
		# self.time.sleep(1)
		# self.driver.find_element_by_link_text("Log In").click()
		self.driver.get("https://www.ahomesteadshoppe.com/index.php?main_page=login")
		self.time.sleep(1)
		self.driver.find_element_by_name("email_address").send_keys(un)
		self.driver.find_element_by_name("password").send_keys(pw)
		self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
		self.time.sleep(1)
		
		#This is used for click options if available then save info 
    def clickbtn(self,btn,item):
	
        opt = []
        optcount = len(btn)
		
        for x in range(optcount):
			#clicker
			b = self.driver.find_elements_by_css_selector("#attrib-6 > option")[x]
			try:
				if b.is_displayed():
					b.click()
					print "Option selected."
					self.time.sleep(1)
				else:
					db = self.save_info()
			except Exception as e:
				print "Option click exception:"+e
			#grabber
			db = self.save_info(item.split("-")[0]+"-"+b.text[b.text.find("(")+1:b.text.find(")")],b.text.split()[-1:][0])
			self.time.sleep(1)
			opt.append(db)
		
        return opt
		
		
		
	    #Special for Janmichaels/Capitol_Imports in case options are available
    def get_info(self,item=None):
		option = []
		try:
			btn = self.driver.find_elements_by_css_selector("#attrib-6 > option")
			print "Btn detected."
			db = self.clickbtn(btn,item)
			option.extend(db) #returns a list of items
		except Exception as e:
			print e
			print "No option detected. Direct info get"
			db = self.save_info(item,self.driver.find_element_by_css_selector("#productPrices > span").text.encode("utf-8"))
			option.append(db)
		return option

    def save_info(self,item=None,price="0"):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#productName").text.encode("utf-8")
        # db.sku = self.driver.find_element_by_css_selector("ul.floatingBox.back li").text.encode("utf-8")
        db.sku = item
        db.cat = "|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("#navBreadCrumb > a")])
        db.desc = self.driver.find_element_by_css_selector("#productDetailsList > li").text.encode("utf-8").split()[1]
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = ""
        db.price1 = price
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "ahs400"
        db.dir160 = "ahs160"
        db.img400 = self.driver.find_element_by_css_selector("#productMainImage a").get_attribute("href")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        try:
			db.option = "|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("#attrib-6 > option")])
        except:
			db.option = "|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("#attrib-6 > option")])
        db.dir800 = "ahs800"
        db.img800 = db.img160
        print db
        # if ".jpg" not in  db.img160:
            # return
        return db
        
        
    def search_item(self,row):
		print "\nSearching for item: " + row+"\n"
		while True:
			try:
				self.driver.find_element_by_name("keyword").send_keys(row.split("-")[0])
				self.driver.find_element_by_name("keyword").send_keys(Keys.ENTER)
				self.time.sleep(self.delay)
				break
			except:
				self.driver.get(self.url)
				self.time.sleep(self.delay)
				continue
		try:
			item = self.driver.find_element_by_css_selector("h3.itemTitle a").get_attribute("href")
			# item = self.driver.find_elements_by_css_selector("#productListing > div.centerBoxWrapperContents > table > tbody > tr > td > div > h3 > a").get_attribute("href")
			print item
			return [item]
		except:
			return None

