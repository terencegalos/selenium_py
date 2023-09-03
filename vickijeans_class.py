from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class vickijeans(domainobject.domainobject):

    vendor = "Vickie Jeans Creations"
    url = "http://www.vickiejeanscreations.com/index.php"
    uname = "Rick"
    passw = "333333"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) center:nth-child(2) b font a:nth-child(6)").click()
        self.time.sleep(1)   
        self.driver.find_element_by_name("bname").send_keys(un)
        self.driver.find_element_by_name("rnumber").send_keys(pw)
        self.driver.find_element_by_css_selector("#signup_form center input[type=\"submit\"]").click()
        self.time.sleep(3)
        print "Success."

    def get_info(self,cat=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) div:nth-child(3) table tbody tr:nth-child(1) td:nth-child(1) span").text.encode("utf-8")
        try:
            db.sku = self.driver.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) div:nth-child(3) table tbody tr:nth-child(1) td:nth-child(2) span").text.encode("utf-8")
        except:
            db.sku = "NO SKU"
        db.cat = cat
        # db.cat = "|".join(cat)
        db.desc = self.driver.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) div:nth-child(3) table tbody tr:nth-child(1) td:nth-child(1) i").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = self.driver.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) div:nth-child(3) table tbody tr:nth-child(2) td span:nth-child(3)").text.encode("utf-8")
        db.price1 = self.driver.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) div:nth-child(3) table tbody tr:nth-child(2) td span:nth-child(1)").text.encode("utf-8")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "VickieJeans400"
        db.dir160 = "VickieJeans160"
        db.img400 = self.driver.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) div:nth-child(3) table tbody tr:nth-child(1) td:nth-child(2) img").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "VickieJeans800"
        db.img800 = db.img160
        print db
        return db

    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        # if len(row.split(",")[1].strip()) > 1:
        while True:
            try:
                self.driver.find_element_by_name("search").clear()
                self.driver.find_element_by_name("search").send_keys(row)
                self.driver.find_element_by_name("search").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except Exception as e:
                print "Search fail:"
                print e
                self.driver.refresh()
                self.time.sleep(1)
                continue
        try:
            items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("body > center > table > tbody > tr > td > center > table > tbody > tr > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > div > a")]
            print items
            return items
        except:
            return None
            

