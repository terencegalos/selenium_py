from helper.table_gateway import gateway
from helper.domainobject import domainobject
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains

class flagsgalore(domainobject):

    vendor = "Flags Galore Decor"
    url = "https://flagsgaloredecorandmore.com/"
    sitemap = "https://www.thecountryhouse.com/site_map.asp"
    uname = "waresitat"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        # print("Logging in.")
        # self.driver.find_element(By.NAME,"username").send_keys(un)
        # self.driver.find_element(By.NAME,"passwd").send_keys(pw)
        # self.driver.find_element(By.NAME,"passwd").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print("Success.")

    def get_info(self,item=None):

        db = gateway()
        db.name = self.driver.find_element(By.XPATH,'//*[@id="bs-7"]/span/div/section/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/div/div/h1').text
        db.sku = self.driver.find_element(By.CSS_SELECTOR,"#bs-8 > span > div > section > div > div > div.x-el.x-el-div.c2-1.c2-2.c2-15.c2-41.c2-3.c2-4.c2-5.c2-6.c2-7.c2-8 > div > div > div:nth-child(1) > div:nth-child(2) > div > div.x-el.x-el-div.c2-1.c2-2.c2-74.c2-3.c2-4.c2-5.c2-6.c2-7.c2-8 > div > div > h1").text.encode("utf-8")
        db.cat = ""
        db.desc = self.driver.find_element(By.CSS_SELECTOR,"#bs-8 > span > div > section > div > div > div.x-el.x-el-div.c2-1.c2-2.c2-15.c2-41.c2-3.c2-4.c2-5.c2-6.c2-7.c2-8 > div > div > div:nth-child(1) > div:nth-child(2) > div > div.x-el.x-el-p.c2-1.c2-2.c2-c.c2-d.c2-40.c2-4v.c2-2b.c2-3.c2-2s.c2-4.c2-1n.c2-5.c2-6.c2-7.c2-8.x-rt").text
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = 1
        db.price1 = 99
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "FlagsGaloreDecor400"
        db.dir160 = "FlagsGaloreDecor160"
        db.img400 = self.driver.find_element(By.CSS_SELECTOR,"#ols-image-wrapper > div > img").get_attribute("src")
        db.img160 = db.img400
        db.desc2 = ""
        db.option = ""
        db.dir800 = "FlagsGaloreDecor800"
        db.img800 = db.img160
        print(db)
        return db
        
        
    def search_item(self,row):
        
        print("\nSearching for item: " + row+"\n")
        
        # ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#n-20492069-utility-menu")).perform()
        # self.time.sleep(1)
        # self.driver.find_element(By.CSS_SELECTOR,"#guacBg15 > div.x-el.x-el-div.c2-1.c2-2.c2-e.c2-39.c2-3.c2-4.c2-5.c2-6.c2-7.c2-8 > a").click()
        # self.driver.find_element(By.CSS_SELECTOR,"body > div > div > div > div.widget.widget-header.widget-header-header-9 > div > div > section > div > div.x-el.x-el-div.c1-1.c1-2.c1-1w.c1-b.c1-c.c1-d.c1-e.c1-f.c1-g > nav.x-el.x-el-nav.c1-1.c1-2.c1-x.c1-t.c1-1x.c1-v.c1-w.c1-b.c1-c.c1-d.c1-4c.c1-e.c1-f.c1-g > div > div > div > div.x-el.x-el-div.c1-1.c1-2.c1-23.c1-t.c1-29.c1-39.c1-5o.c1-5p.c1-b.c1-c.c1-d.c1-e.c1-f.c1-g > div").click()
        # self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#bs-4 > span > div > div > div > svg")).perform()
        # ActionChains(self.driver).move_to_element(self.driver.find_element(By.XPATH,'//*[@id="bs-4"]/span/div/div/div/div/svg')).perform()
        # self.time.sleep(1)
        # self.driver.find_element(By.CSS_SELECTOR,"#bs-4").click()
        # self.driver.find_element(By.NAME,"keywords").send_keys(str(row))
        # self.driver.find_element(By.NAME,"keywords").send_keys(self.Keys.ENTER)
        self.driver.get(f"https://flagsgaloredecorandmore.com/shop?olsPage=search&keywords={str(row)}&sortOption=descend_by_match")
        
        self.time.sleep(1)

        try:
            result = WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="bs-7"]/span/div/section/div/div/div[3]/div/div/div/div[2]/div[2]/div/div[1]/div/a'))).get_attribute("href")
            # self.driver.find_element(By.XPATH,'//*[@id="bs-7"]/span/div/section/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a').click()
            self.time.sleep(1)
            return [result]
        except:
            print(f"No result?")
            return None

# ongoing dev
def get_cat(self):
    all = ["http://www.thecountryhouse.com/viewcategory.asp?catid=126","http://www.thecountryhouse.com/viewcategory.asp?catid=125","http://www.thecountryhouse.com/viewcategory.asp?catid=93","http://www.thecountryhouse.com/viewcategory.asp?catid=100","http://www.thecountryhouse.com/viewcategory.asp?catid=112","http://www.thecountryhouse.com/viewcategory.asp?catid=153"]
    cats = self.driver.find_elements(By.CSS_SELECTOR,"#content > table > tbody > tr:nth-child(1) > td:nth-child(2) > strong:nth-child(2) > a")
    cats = self.driver.find_elements(By.CSS_SELECTOR,"#content > table > tbody > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(24) > a")
    cats = self.driver.find_elements(By.CSS_SELECTOR,"#content > table > tbody > tr:nth-child(1) > td:nth-child(3) > strong:nth-child(30) > a")
    cats = self.driver.find_elements(By.CSS_SELECTOR,"#content > table > tbody > tr:nth-child(1) > td:nth-child(3) > strong:nth-child(32) > a")