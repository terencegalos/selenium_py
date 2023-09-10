from table_gateway import gateway
import domainobject

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class cowgirl(domainobject.domainobject):

    vendor = "Cowgirl Chocolates"
    url = "https://www.cowgirlchocolates.com/"
    home = "https://www.cowgirlchocolates.com/"
    uname = "service@waresitat.com"
    passw = "wolfville1"
    delay = 1
    
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element_by_css_selector("body > header > nav > div > ul > li.navUser-item.navUser-item--account > a.navUser-action.navUser-action-login").click()
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#sw_dropdown_778 > a")).perform()
        # self.time.sleep(1)
        print "Logging in..."
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login_email"))).send_keys(un)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login_pass"))).send_keys(pw)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login_pass"))).send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("body > div.body > div.container > div > div.productView > section:nth-child(1) > div > h1").text.encode("utf-8")
        try:
            db.sku = self.driver.find_element_by_css_selector("body > div.body > div.container > div > div.productView > section:nth-child(1) > div > dl > dd").text.encode("utf-8")
        except:
            db.sku = "No sku."
            
        db.cat = "|".join([c.text.encode("utf-8") for c in self.driver.find_elements_by_css_selector("body > div.body > div.container > ul > li > a")])
        db.desc = self.driver.find_element_by_css_selector("#tab-description").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
			db.min1 = self.driver.find_element_by_css_selector("body > div.body > div.container > div > div.productView > section:nth-child(3) > div.productView-options > form:nth-child(1) > div.form-field.form-field--increments > div input").get_attribute("value")
        except:
			db.min1 = ""
        db.price1 = self.driver.find_element_by_css_selector("body > div.body > div.container > div > div.productView > section:nth-child(1) > div > div.productView-price > div > span").text.encode("utf-8")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "cowgirl400"
        db.dir160 = "cowgirl160"
        self.time.sleep(4)
        db.img400 = self.driver.find_element_by_css_selector("body > div.body > div.container > div > div.productView > section.productView-images > figure > div > a > img").get_attribute("src")
        # print db.img400
        # db.img400 = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.NAME, "div > img.fotorama__img"))).get_attribute("src")
        # print db.img400
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        try:
			db.option = "|".join([opt.text for opt in self.driver.find_elements_by_css_selector("body > div.body > div.container > div > div.productView > section:nth-child(3) > div.productView-options > form:nth-child(1) > div:nth-child(3) > div > select > option")])
        except:
			db.option = ""
        db.dir800 = "cowgirl800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        # while True:
            # try:
        self.driver.find_element_by_css_selector("#menu > nav > ul:nth-child(2) > li:nth-child(8) > a").click()
        self.time.sleep(2)
        # print self.driver.find_element_by_css_selector("#quickSearch > div > form > fieldset > div").get_attribute("innerHTML")
        self.driver.find_element_by_css_selector("#quickSearch > div > form > fieldset > div > input").clear()
        self.driver.find_element_by_css_selector("#quickSearch > div > form > fieldset > div > input").send_keys(row)
        self.driver.find_element_by_css_selector("#quickSearch > div > form > fieldset > div > input").send_keys(Keys.ENTER)
        self.time.sleep(1)
				# break
            # except:
                # self.driver.refresh()
                # self.time.sleep(1)
                # continue
        try:
            item = self.driver.find_element_by_css_selector("#product-listing-container > form:nth-child(2) > ul > li > article > div > h3 > a").get_attribute("href")
            print item
            return [item]
        except:
            return None