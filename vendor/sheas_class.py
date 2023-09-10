from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class sheas(domainobject.domainobject):

    vendor = "Shea's Wildflower Company"
    url = "https://sheaswildflowers.com/Scripts/PublicSite/index.php"
    home = "https://sheaswildflowers.com/Scripts/PublicSite/index.php"
    uname = "waresitat"
    passw = "wolfville"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element_by_css_selector("#menu > ul > li:nth-child(6) > a").click()
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#sw_dropdown_778 > a")).perform()
        # self.time.sleep(1)
        print "Logging in..."
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(un)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(pw)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(Keys.ENTER)
        # self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#popupwrapper > table > tbody > tr:nth-child(1) > td > strong").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#descCell > p.sku").text.encode("utf-8")
        db.cat = ""
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
        db.dir400 = "Sheas400"
        db.dir160 = "Sheas160"
        self.time.sleep(4)
        db.img400 = self.driver.find_element_by_css_selector("#imgCell > img").get_attribute("src")
        # print db.img400
        # db.img400 = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.NAME, "div > img.fotorama__img"))).get_attribute("src")
        # print db.img400
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Sheas800"
        db.img800 = db.img160
        print db
        self.driver.back()
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        # while True:
            # try:
        self.driver.find_element_by_css_selector("input.button").clear()
        self.driver.find_element_by_css_selector("input.button").send_keys(row)
        self.driver.find_element_by_css_selector("input.button").send_keys(Keys.ENTER)
        self.time.sleep(1)
				# break
            # except:
                # self.driver.refresh()
                # self.time.sleep(1)
                # continue
        try:
            item = self.driver.find_element_by_css_selector("#product > div > a").get_attribute("href")
            print item
            return [item]
        except:
            return None