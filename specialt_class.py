from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class specialt(domainobject.domainobject):

    vendor = "Special T Imports"
    # url = "https://sti.specialtimports.com/Products"
    url = "http://www.specialtimports.com/"
    sitemap = "https://www.thecountryhouse.com/site_map.asp"
    uname = "waresitat"
    passw = "wolfville"
    delay = 1
    # dbs = []
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("username").send_keys(un)
        # self.driver.find_element_by_name("passwd").send_keys(pw)
        # self.driver.find_element_by_name("passwd").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        result = self.driver.find_elements_by_css_selector("div.text-center")
        print "Result count:"+str(len(result))
        if len(result) == 0: #return if no results
            return

        db = gateway()
        db.name = result[0].find_element_by_css_selector("p:nth-child(3)").text.encode("utf-8")
        db.sku = result[0].find_element_by_css_selector("strong.text-dark").text.encode("utf-8")
        db.cat = ""
        db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = result[0].find_element_by_css_selector("p:nth-child(3)").text.encode("utf-8").splitlines()[-1]
        db.seller = ""
        db.min1 = 1
        db.price1 = 99
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "specialtimports400"
        db.dir160 = "specialtimports160"
        db.img400 = result[0].find_element_by_css_selector("img.img-fluid").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "specialtimports800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        # while True:
        #     try:
        self.driver.find_element_by_css_selector("input[type=text]").clear()
        self.driver.find_element_by_css_selector("input[type=text]").send_keys(str(row))
        self.driver.find_element_by_css_selector("#app > div.top > div.search.d-lg-flex.d-none > div").click()
        self.time.sleep(1)
            #     break
            # except:
            #     self.driver.refresh()
            #     self.time.sleep(1)
            #     continue

        # item = self.driver.find_element_by_css_selector("#app > div.top > div.search.d-lg-flex.d-none > div > div > img").
        return None
