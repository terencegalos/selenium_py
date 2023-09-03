from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class timeless(domainobject.domainobject):

    vendor = "Timeless By Design"
    url = "http://timelessbydesign.com/"
    search = "https://www.blossombucket.com/shop/"
    home = "http://timelessbydesign.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("log").send_keys(un)
        # self.driver.find_element_by_name("pwd").send_keys(pw)
        # self.driver.find_element_by_name("pwd").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        # db.name = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#popupwrapper > table > tbody > tr:nth-child(1) > td > strong"))).text.encode("utf-8")
        try:
			db.name = self.driver.find_element_by_css_selector("#div__body > div > div.container > div:nth-child(2) > div.col-sm-8 > div > div.prod-des > h2").text.encode("utf-8")
        except:
			return None
        try:
			db.sku = self.driver.find_element_by_css_selector("#div__body > div > div > div:nth-child(2) > div.col-sm-8 > div > div.prod-des > h5 > b").text.encode("utf-8").split()[-1:][0]
        except:
			db.sku = self.driver.find_element_by_css_selector("#div__body > div > div.container > div:nth-child(2) > div.col-sm-8 > div > div.prod-des > div.d-box > p:nth-child(3)").text.encode("utf-8").split()[-1:]
        db.cat = "|".join([i.text for i in self.driver.find_elements_by_css_selector("#div__header > div.container.bread > a")])
        db.desc = self.driver.find_element_by_css_selector("#div__body > div > div.container > div:nth-child(2) > div.col-sm-8 > div > div.prod-info > div:nth-child(8) > span.info-span2").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element_by_css_selector("#div__body > div > div.container > div:nth-child(2) > div.col-sm-8 > div > div.prod-info > div:nth-child(3) > span.info-span2").text.encode("utf-8")
        db.seller = ""
        db.min1 = ""
        db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "Timeless400"
        db.dir160 = "Timeless160"
        db.img400 = self.driver.find_element_by_css_selector("#thumbCell1a").get_attribute("href")
        db.img160 = db.img400.split("/")[-1:][0] #if ".jpg?" not in db.img400.split("/")[-1:][0] else (db.img400.split("/")[-1:][0]).split("?")[0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Timeless800"
        db.img800 = db.img160     
        print db
        self.driver.back()
        return db
        
        
    def search_item(self,row):
        print "\nSearching for item: " + row+"\n"
        self.driver.find_element_by_css_selector("#search-bt > i").click()
        self.time.sleep(1)
        while True:
            try:
                self.driver.find_element_by_id("searchtxtn").clear()
                self.driver.find_element_by_id("searchtxtn").send_keys(row)
                self.driver.find_element_by_id("searchtxtn").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            except Exception as e:
                print "Search failed:"
                self.driver.get(self.home)
                print e
                self.time.sleep(1)
                continue

        try:
			item = self.driver.find_element_by_css_selector("#handle_itemMainPortlet > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > div > div > table > tbody > tr > td > table > tbody > tr > td.one > div > div:nth-child(2) > a").get_attribute("href")
			return [item]
        except:
			return None