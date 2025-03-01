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
        
        file_path = os.path.join(os.path.dirname(__file__),"csv","outfile","noimg",vendor.replace("/","&")+".csv")
        with open(file_path,'r') as fopen:
            reader = csv.reader(fopen)
            out = [line[0] for line in reader if len(line)]
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
                
        
        
    def send_to_file(self, vendor, dbs):
        gt = [db.retrieve() for db in dbs]

        # Construct the file path using os.path.join
        file_path = os.path.join(os.path.dirname(__file__), "csv", "outfile", f"{vendor} output.csv")

        with open(file_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(gt)