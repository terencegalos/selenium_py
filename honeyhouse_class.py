from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class honeyhouse(domainobject.domainobject):

    vendor = "Honey House Naturals"
    url = "http://www.honeyhousenaturals.com/16/home.htm"
    uname = "waresitat"
    passw = "wolfville"
    delay = 1
    links = []
    count = 0
    
        
    def nextPage(self):
        pages = self.driver.find_elements_by_css_selector("#COMSrchPageTop > a")
        if self.count >= len(pages):
            print "Page exhausted."
            return False

        self.driver.find_elements_by_css_selector("#COMSrchPageTop > a")[self.count].click()
        self.time.sleep(1)
        self.count += 1
        return True
        

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element_by_css_selector("#container table tbody tr:nth-child(1) td div table tbody tr td div.utilitynav a:nth-child(2)").click()
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("UserName").send_keys(un)
        self.driver.find_element_by_name("Password").send_keys(pw)
        self.driver.find_element_by_name("Password").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."
		
	#This is used for click options if available then save info 
    def clickbtn(self,btn):
	
        opt = []
        optcount = len(btn)
		
        for x in range(optcount):
			try:
				b = self.driver.find_elements_by_css_selector("table > tbody > tr:nth-child(2) > td > select > option")[x]
				if b.is_displayed():
					b.click()
					print "Option selected."
					self.time.sleep(1)
				else:
					db = self.save_info()
			except Exception as e:
				print "Option click exception:"+e
			db = self.save_info()
			self.time.sleep(1)
			opt.append(db)
		
        return opt
		
		
		
	    #Special for Janmichaels/Capitol_Imports in case options are available
    def get_info(self,item=None):
		option = []

		try:
			btn = self.driver.find_elements_by_css_selector("table > tbody > tr:nth-child(2) > td > select > option")
			print "Btn detected."
			db = self.clickbtn(btn)
			option.extend(db) #returns a list of items
		except Exception as e:
			print e
			print "No option detected. Direct info get"

		db = self.save_info(item)
		option.append(db)
		return option
            
        

    def save_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element_by_css_selector("div.COMProductName").text.encode("utf-8")
        except:
            return None

        db.sku = self.driver.find_element_by_id("CurrentItemDiv").text.encode("utf-8")
        db.cat = self.driver.find_element_by_css_selector("#commerce > div.COMCatHeader > h1").text.encode("utf-8")
        try:
            db.desc = self.driver.find_element_by_css_selector("#commerce > div:nth-child(2) > div.COMProdDesc").text.encode("utf-8")
        except:
            db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
			db.min1 = self.driver.find_element_by_css_selector("#QtyBox input:nth-child(1)").get_attribute("value")
        except:
			db.min1 = ""
        try:
			db.price1 = self.driver.find_element_by_css_selector("#ProductPrice").text.encode("utf-8")
        except:
			try:
				db.price1 = self.driver.find_element_by_css_selector("#ProductDiscount").text.encode("utf-8")
			except:
				print "No price detected."
				return None
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "honeyhouse400"
        db.dir160 = "honeyhouse160"
        db.img400 = self.driver.find_element_by_id("COMProdImage").get_attribute("src")
        if "nophoto" in db.img400:
            print "No photo detected."
            return None
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        try:
			db.option = "|".join([i.text for i in self.driver.find_elements_by_css_selector("div.ProdGridDiv > div.ProdGridName > a")])
        except:
			db.option = ""
            
        db.dir800 = "honeyhouse800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_id("SearchText").clear()
                self.driver.find_element_by_id("SearchText").send_keys(str(row))
                self.driver.find_element_by_id("SearchText").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.get(self.url)
                self.time.sleep(1)
                continue

        self.links = []
        item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#container > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > div > div > table > tbody > tr > td > div.quickorderproductname > a") if a.get_attribute("href") not in self.links]
        print item
        self.links.extend(item)
        while self.nextPage():
            item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#container > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > div > div > table > tbody > tr > td > div.quickorderproductname > a") if a.get_attribute("href") not in self.links]
            print item
            self.links.extend(item)

        return self.links

