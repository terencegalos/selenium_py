from table_gateway import gateway
import domainobject

class adamsco_repair(domainobject.domainobject):

    vendor = "Adams_and_Company"
    url = "https://adamsandco.net/home.php"
    uname = "service@waresitat.com"
    passw = "wolfville"
    delay = 1
    table = []
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # self.driver.find_element_by_css_selector("#header div ul li:nth-child(1) a").click()
        # self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("username").send_keys(un)
        # self.driver.find_element_by_name("password").send_keys(pw)
        # self.driver.find_element_by_css_selector("input.formbutton").click()
        # self.time.sleep(1)
        # self.driver.get(self.url)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = []
        try:
            name = self.driver.find_element_by_css_selector("body div.product.container div div:nth-child(1) div.summary.col-tablet-7 h1").text.encode("utf-8")
        except:
            print "Name not detected"
            name = "No name."
        sku = ""
        cat = ""
        # try:
            # rows = self.driver.find_elements_by_css_selector("body div.product.container div div tbody tr")
            # d = []
            # for row in rows:
                # info = row.find_elements_by_css_selector("td")
                # data = ":".join([i.text.encode("utf-8") for i in info])
                # d.append(data.replace("::",":"))
            # desc = "-".join(d.replace(",","/comma"))
        # except:
            # print "Table not detected. No desc."
            # desc = ""
        desc = ""
        stock = ""
        sale = ""
        set = ""
        custom = ""
        size = ""
        seller = ""
        min1 = ""
        price1 = ""
        min2 = ""
        price2 = ""
        min3 = ""
        price3 = ""
        multi = ""
        dir400 = "Adams400"
        dir160 = "Adams160"
        img400 = self.driver.find_element_by_css_selector("#main_image img:nth-child(1)").get_attribute("src")
        img160 = img400.split("/")[-1:][0]
        desc2 = ""
        option = ""
        dir800 = "Adams800"
        img800 = img160
        #print db
        if "adams_no_image" not in img400:
            db.append([name,sku,cat,desc,stock,sale,set,custom,size,min1,price1,min2,price2,min3,price3,multi,dir400,dir160,img400,img160,desc2,option,dir800,img800])
            print db[0]
            self.table.append(db[0])
            return self.table
        else:
			print "No image detected."
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("query").clear()
                self.driver.find_element_by_name("query").send_keys(str(row))
                self.driver.find_element_by_name("query").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                continue

        items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("body div.category.container div div.products.list.col-tablet-9 div.product.container-fluid div div.summary.col-tablet-8.col-phone-7 div a")]
        return items

