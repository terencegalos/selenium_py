# from active_record import active_record as ac
import csv, os
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class domainobject():
    import time
    
    def __init__(self,driver):
        self.driver = driver
        self.init_login(self.uname,self.passw)
        self.time.sleep(1)
    
    def navigate(self,item):
        try:
            print(item)
            self.driver.get(item)
            self.time.sleep(self.delay)
            # self.driver.execute_script("window.stop();")
        except Exception as e:
            print(e)
            print("Clicking found item.")
            item.click()
            self.time.sleep(self.delay)
        
    def get_missing(self,vendor):
        print(vendor)
        fopen = open(os.path.dirname(__file__)+"/csv/outfile/noimg/"+vendor.replace("/","&")+".csv","r")
        res = csv.reader(fopen.read().splitlines())
        out = [line[0] for line in res if len(line)]
        return out
        
    def results(self,items):
        if items is None or len(items) == 0:
            print("Not an item list")
            return False
        return True
            
    def get_items(self,items):
        for item in items:
            self.navigate(item)
            try:
                self.save_info(item,table)            
            except:
                print("Item not found. Getting next item...")
                
    def send_to_file(self,vendor,dbs):
        gt = [db.retrieve()for db in dbs]
        outfile = open(os.path.dirname(__file__)+"/csv/outfile/"+vendor+" output.csv","w")
        writer = csv.writer(outfile)
        writer.writerows(gt)