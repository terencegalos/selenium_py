from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re


class ahs(domainobject.domainobject):

    vendor = "A Homestead Shoppe"
    url = "http://www.ahomesteadshoppe.com/"
    home = "http://www.ahomesteadshoppe.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    links = []

    def nextPage(self):
        try:
            self.driver.find_elements_by_css_selector(
                "a[title=' Next Page ']")[-1].click()
            self.time.sleep(1)
            return True
        except:
            print "Page exhausted."
            return False

    def init_login(self, un, pw):
        self.driver.get(
            "https://www.ahomesteadshoppe.com/index.php?main_page=login")
        self.time.sleep(1)
        self.driver.find_element_by_name("email_address").send_keys(un)
        self.driver.find_element_by_name("password").send_keys(pw)
        self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
        self.time.sleep(1)

        #This is used for click options if available then save info
    def clickbtn(self, btn, item):

        opt = []
        optcount = len(btn)
        print optcount
        print "Btn length confirmed."

        for x in range(optcount):
            print x
            print "Click attempt."
            try:
                b = self.driver.find_elements_by_css_selector(
                    "#attrib-6 > option")[x]
                if b.is_displayed():
                    b.click()
                    print "Option selected."
                    self.time.sleep(1)
                    curropt = b.text
                    match = re.search('\(.+?\)', curropt)
                    print "regex result" + match.group()
                    db = self.save_info(
                        re.search('\(.+?\)', curropt).group(), curropt)
                    opt.append(db)
            except Exception as e:
                print "Option click exception:" + e

            opt.append(db)

        return opt

#Special for Janmichaels/Capitol_Imports in case options are available

    def get_info(self, item=""):
        option = []

        try:
            btn = self.driver.find_elements_by_css_selector(
                "#attrib-6 > option")
            if len(btn) == 0:
                raise
            print "Btn detected."
            db = self.clickbtn(btn, item)
            option.extend(db)  #returns a list of items
        except Exception as e:
            print e
            print "No option detected. Direct info get"
            db = self.save_info(item)
            option.append(db)

        return option

    def save_info(self, part="", price=""):
        db = gateway()
        try:
            db.name = self.driver.find_element_by_css_selector(
                "#productName").text.encode("utf-8") + " - " + " ".join(
                    price.split()[:-1])
        except:
            self.time.sleep(1)
            self.driver.refresh()
            self.time.sleep(1)
            db.name = self.driver.find_element_by_css_selector(
                "#productName").text.encode("utf-8") + " - " + " ".join(
                    price.split()[:-1])

        try:
            db.sku = self.driver.find_element_by_css_selector(
                "#productDetailsList > li").text.split()[1].strip(
                    "#") + "-" + "".join(part.split()).strip(")").strip(
                        "(")  # add option code if available
            # self.driver.find_element_by_css_selector("#productDetailsList > li").text.encode("utf-8").split()[1].strip("#")
        except:
            return None

        db.cat = "|".join([
            i.text.encode("utf-8") for i in
            self.driver.find_elements_by_css_selector("#navBreadCrumb > a")
        ])
        db.desc = part
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
            td1 = self.driver.find_element_by_css_selector(
                "#productQuantityDiscounts > table > tbody > tr:nth-child(2) > td:nth-child(1)"
            ).text.encode("utf-8")
            db.min1 = "".join(td1.split()[0])
            db.price1 = td1.split()[1].strip("$")
            td2 = self.driver.find_element_by_css_selector(
                "#productQuantityDiscounts > table > tbody > tr:nth-child(2) > td:nth-child(2)"
            ).text.encode("utf-8")
        except:
            try:
                db.min1 = self.driver.find_element_by_css_selector(
                    "#cartAdd > input[type=text]:nth-child(3)").get_attribute(
                        "value")
            except:
                db.min1 = 1
            try:
                db.price1 = self.driver.find_element_by_css_selector(
                    "#productPrices > span").text.encode("utf-8").strip("$")
            except:
                try:
                    db.price1 = price.split()[-1]
                except:
                    return None
        try:
            db.min1 = "".join(
                [db.min1 if "-" not in db.min1 else db.min1.split("-")[0]])
        except:
            pass

        try:
            db.min2 = td2.split()[0].strip("+")
            db.price2 = td2.split()[1].strip("$")
        except:
            db.min2 = ""
            db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "ahs400"
        db.dir160 = "ahs160"
        db.img400 = self.driver.find_element_by_css_selector(
            "#productMainImage a").get_attribute("href")
        db.img160 = db.img400.split("/")[-1:][0]
        try:
            db.desc2 = self.driver.find_element_by_css_selector(
                "#productDescription").text.encode("utf-8")
        except:
            db.desc2 = ""
        db.option = "|".join([
            i.text.encode("utf-8") for i in
            self.driver.find_elements_by_css_selector("#attrib-6 > option")
        ])
        db.dir800 = "ahs800"
        db.img800 = db.img160
        print db
        return db

    def search_item(self, row):

        print "\nSearching for item: " + row + "\n"
        self.driver.find_element_by_name("keyword").send_keys(
            row.split("-")[0])
        self.driver.find_element_by_name("keyword").send_keys(Keys.ENTER)
        self.time.sleep(self.delay)
        try:
            self.links = []
            item = [
                i.get_attribute("href") for i in
                self.driver.find_elements_by_css_selector("h3.itemTitle a")
            ]
            print item
            self.links.extend(item)
            while self.nextPage():
                item = [
                    i.get_attribute("href") for i in
                    self.driver.find_elements_by_css_selector("h3.itemTitle a")
                ]
                print item
                self.links.extend(item)
            return self.links
        except:
            return None
