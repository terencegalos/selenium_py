from table_gateway import gateway
import sys
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# reload(sys)
# sys.setdefaultencoding("utf-8")

class exhibitors(domainobject.domainobject):

    vendor = "Exhibitors"
    url = "https://www.lasvegasmarket.com/exhibitor-directory"
    search = "https://www.lasvegasmarket.com/exhibitor-directory"
    home = "https://www.lasvegasmarket.com/exhibitor-directory"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.home)
        self.searchMatch()

    def get_info(self,item=None):
        print "Injected: "+item
        btns = self.driver.find_elements_by_css_selector("ul#s_results li")
        for btn in btns:
            if item in btn.find_element_by_css_selector("span:first-child").text.encode("utf-8"):
                self.time.sleep(2)
                print "Match found."
                btn.find_element_by_css_selector("span:first-child").click()
                # self.time.sleep(5)
                rbtn = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"ul#s_results li.active div.tab-content-top")))
                # rbtn = self.driver.find_element_by_css_selector("ul#s_results li.active div.tab-content-top")
                db = gateway()
                name = rbtn.find_element_by_css_selector("p > strong").text.encode("utf-8")
                if "Represented By:" not in name:
                    db.name = name
                else:
                    db.name = rbtn.find_element_by_css_selector("p").text.encode("utf-8")
                db.sku = item
                db.cat = "|".join([c.text.encode("utf-8") for c in rbtn.find_elements_by_css_selector("p.address")])
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
                db.dir400 = ""
                db.dir160 = ""
                db.img400 = ""
                db.img160 = ""
                db.desc2 = ""
                db.option = ""
                db.dir800 = ""
                db.img800 = ""
                print db
                # if ".jpg" not in  db.img160:
                    # return
                return db
            else:
                print "No match."
        
    def save_info(self,item):
        print "Initializing gateway..."
        db = gateway()
        # print item.get_attribute("innerHTML")
        # db.name = WebDriverWait(item,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR," p > strong"))).text.encode("utf-8")
        db.name = item.find_element_by_css_selector("p > strong").text.encode("utf-8")
        print db.name
        db.sku = ""
        try:
            db.cat = "|".join([c.text.encode("utf-8") for c in item.find_elements_by_css_selector("p.address")])
        except:
            db.cat = item.find_element_by_css_selector("p:nth-child(1)")
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
        db.dir400 = ""
        db.dir160 = ""
        db.img400 = ""
        db.img160 = ""
        db.desc2 = ""
        db.option = ""
        db.dir800 = ""
        db.img800 = ""
        print db
        # if ".jpg" not in  db.img160:
            # return
        return db
        
        
    def searchMatch(self):
        match = self.driver.find_element_by_css_selector("#exact")
        match.click()
        self.time.sleep(1)
            
    def search_item(self,row):
		print "\nSearching for item: " + row+"\n"
		try:
			inp = self.driver.find_element_by_css_selector("#main-search-form-box")
			inp.clear()
			inp.send_keys(row.encode("utf-8"))
			inp.send_keys(Keys.ENTER)
			self.time.sleep(1.5)
		except Exception as e:
			print "Search failed:"
			self.driver.get(self.search)
			print e
			self.time.sleep(1)
			self.searchMatch()
			self.time.sleep(1)
		
		return None