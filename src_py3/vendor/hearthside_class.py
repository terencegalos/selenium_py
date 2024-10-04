from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class hearthside(domainobject):
    
    def __init__(self,driver,scraper_mode):
        super().__init__(driver)
        self.mode = scraper_mode
        

    vendor = "The Hearthside Collection"
    url = "https://thehearthsidecollection.com/shop/"
    home = "https://thehearthsidecollection.com/shop/"
    uname = "rick@shophereshopthere.com"
    passw = "wolfville"
    delay = 1
    lastStop = "https://www.thehearthsidecollection.com/shop/col-house-designs/home-block-3-asstd./"
    flag = False
    links = []
        

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        print("Logging in.")
        self.driver.find_element(By.CSS_SELECTOR,"#sw_dropdown_278 > a > span").click()
        self.time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR,"#account_info_278 > div.ty-account-info__buttons.buttons-container > a.cm-dialog-opener.cm-dialog-auto-size.ty-btn.ty-btn__secondary").click()
        # self.time.sleep(1)
		
        self.driver.find_element(By.NAME,"user_login").send_keys(un)
        self.driver.find_element(By.NAME,"password").send_keys(pw)
        while True:
            inp = input("Enter yes if done (dont click submit)")
            if inp == "yes":
                self.driver.find_element(By.NAME,"password").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            else:
                continue
        print("Success.")

    def get_info(self,item=None):
        db = gateway()
        # db.name = self.driver.find_element(By.CSS_SELECTOR,"#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(2) > div > div > div > div > div.ty-product-block__left > form > h1").text.encode("utf-8")
        # db.sku = self.driver.find_element(By.CSS_SELECTOR,"#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(2) > div > div > div > div > div.ty-product-block__left > form > div.ty-product-block__sku span").text.encode("utf-8")
        try:
            db.name = self.driver.find_element(By.CSS_SELECTOR,"#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(2) > div > div.ty-product-bigpicture > div.ty-product-bigpicture__left > div > h1").text
        except:
            self.driver.get(self.url)
            self.time.sleep(1)
            print("No name detected.")
            return
        db.sku = self.driver.find_element(By.CSS_SELECTOR,"#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(2) > div > div.ty-product-bigpicture > div.ty-product-bigpicture__right > form > div.ty-product-bigpicture__sidebar-bottom > div.ty-product-block__sku > div > span").text
        db.cat = "|".join([a.text for a in self.driver.find_elements(By.CSS_SELECTOR,"#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(1) > div > div > div > a")])
        db.desc = self.driver.find_element(By.CSS_SELECTOR,"#content_description").text
        # db.stock = self.driver.find_element(By.CSS_SELECTOR,"#commerce > div > table > tbody > tr > td:nth-child(2) > table:nth-child(1) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(3) > td:nth-child(2)").text.encode("utf-8")
        db.stock = ""
        try:
            db.price1 = self.driver.find_element(By.CSS_SELECTOR,"#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(2) > div > div.ty-product-block.ty-product-detail > div.ty-product-block__wrapper.clearfix > div.ty-product-block__left > form > div.prices-container.price-wrap > div > span:nth-child(1) > span > span.ty-strike > span:nth-child(2)").text
            db.sale = self.driver.find_element(By.CSS_SELECTOR,"#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(2) > div > div.ty-product-block.ty-product-detail > div.ty-product-block__wrapper.clearfix > div.ty-product-block__left > form > div.prices-container.price-wrap > div > div").text.strip("$")
        except:
            db.sale = ""
            try:
                db.price1 = self.driver.find_element(By.CSS_SELECTOR,"#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(2) > div > div.ty-product-bigpicture > div.ty-product-bigpicture__right > form > div.prices-container.price-wrap > div > div > span > span > span:nth-child(2)").text
            except:
                print("No price detected")
                return None
        try:
            db.min2 = self.driver.find_element(By.CSS_SELECTOR,"#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(2) > div > div.ty-product-bigpicture > div.ty-product-bigpicture__right > form > div.ty-product-bigpicture__sidebar-bottom > div.ty-product-block__field-group > div > div.ty-qty-discount > table > thead > tr > th:nth-child(2)").text.split("+")[0]
            db.price2 = self.driver.find_element(By.CSS_SELECTOR,"#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(2) > div > div.ty-product-bigpicture > div.ty-product-bigpicture__right > form > div.ty-product-bigpicture__sidebar-bottom > div.ty-product-block__field-group > div > div.ty-qty-discount > table > tbody > tr > td:nth-child(2) > span").text
        except:
            db.min2 = ""
            db.price2 = ""
        # else:
			# return None
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
            db.min1 = self.driver.find_element(By.CSS_SELECTOR,"#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(2) > div > div.ty-product-bigpicture > div.ty-product-bigpicture__right > form > div.ty-product-bigpicture__sidebar-bottom > div.ty-product-block__field-group > div > div.ty-qty.clearfix.changer > div > input").get_attribute("value")
        except:
            db.min1 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty.clearfix.changer > select > option:nth-child(1)").get_attribute("value")
        # db.price1 = self.driver.find_element(By.CSS_SELECTOR,"span.ty-price-num").text.encode("utf-8")
        # db.min2 = self.driver.find_element(By.CSS_SELECTOR,"div > div.ty-qty-discount > table > thead > tr > th:nth-child(2)").text.encode("utf-8").split("+")[1]
        # db.price2 = self.driver.find_element(By.CSS_SELECTOR,"div > div.ty-qty-discount > table > tbody > tr > td:nth-child(2) > span").text.encode("utf-8")
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "Hearthside400"
        db.dir160 = "Hearthside160"
        try:
            # click 2nd photo option
            self.driver.find_element(By.CSS_SELECTOR,"#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(2) > div > div.ty-product-bigpicture > div.ty-product-bigpicture__left > div > div > div.ty-product-thumbnails.ty-center.cm-image-gallery > a:nth-child(2) > img").click()
            self.time.sleep(1)
        except:
            pass
        try:
            db.img400 = self.driver.find_element(By.XPATH,'//*[@id="tygh_main_container"]/div[3]/div/div[2]/div/div[1]/div[2]/div/div/div[2]/a[2]/img').get_attribute("src").replace('thumbnails/55/55/','')
            
        except:
            db.img400 = "NA"
            
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Hearthside800"
        db.img800 = db.img160
        print(db)
        self.time.sleep(1)

        return db
        
    def nextPage(self):
        content = self.driver.find_elements(By.CSS_SELECTOR,"#pagination_contents > div.ty-pagination__bottom > div > a")[-1:][0]
        if "-" in content.text:# and content.text.split()[0] != content.text.split()[-1]:
            print(content.text.split()[0])
            print(content.text.split()[-1])
            while True:
                try:
                    node = self.driver.find_element(By.CSS_SELECTOR,"a.ty-pagination__next")
                    node.click()
                    self.driver.execute_script("window.onload = function () {document.querySelector('body');}");
                    break
                except:
                    self.driver.refresh()
                    self.time.sleep(1)
                    continue
            self.time.sleep(5)
            return True
        else: 
            print("No more pages.***")
            return False
        return True
        # try:
        #     node = self.driver.find_element(By.CSS_SELECTOR,"a.ty-pagination__next")
        #     node.click()
        #     self.time.sleep(3)
        #     return True
        # except:
        #     print "No more pages.***"
        #     return False
        
    def search_item(self,row):
        print("\nSearching for item: " + row+"\n")

        # try:
        #     search = self.driver.find_element(By.NAME,"hint_q")
        # except:
        #     search = self.driver.find_element(By.NAME,"q")
		
        # search.clear()
        # search.send_keys(str(row))
        # search.send_keys(Keys.ENTER)
        # search.click()
        # self.time.sleep(1)
		
        # items = []
        # page = self.driver.find_element(By.CSS_SELECTOR,"#pagination_contents > div.grid-list > div:nth-child(1) > div > form > div.ty-grid-list__image > div > div > div.owl-wrapper-outer > div > div:nth-child(1) > div > a").get_attribute("href")
        try:
            self.driver.get(f"https://www.thehearthsidecollection.com/shop/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&q={row}&dispatch=products.search")
            item = self.driver.find_element(By.XPATH,'//*[@id="pagination_contents"]/div[2]/div[1]/div/form/div[2]/a').get_attribute('href')
            print(item)
            # WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.snize-ac-results.snize-new-design > div.snize-ac-results-content > ul.snize-ac-results-list.snize-ac-results-list-last > li.snize-product.snize-product-in-stock.snize-ac-odd > a'))).click()
            # self.time.sleep(1)
            # print page
            # items.extend(page)

            # while self.nextPage():
            #     try:
            #         page = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"div > a.product-title")]
            #     except:
            #         self.driver.refresh()
            #         self.time.sleep(1)
            #         page = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"div > a.product-title")]
            #     print page
            #     items.extend(page)

            return [item]
        except:
             return None