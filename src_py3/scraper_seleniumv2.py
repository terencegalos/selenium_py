import sys
import csv,os,time#,imp
from datetime import datetime
import importlib.util

# Custom modules
from helper.active_record import ActiveRecord
import helper.webdriver_config as webdriver_config


# Class for keeping track of the subtotal
class Counter:
    def __init__(self):
        self.subtotal = 0


# Main class for scraping
class Scraper:
    def __init__(self, vendor_name):
        self.browser = webdriver_config.init_driver()
        self.vendor_name = vendor_name
        
        # Import the vendor-specific class
        # contruct path
        vendor_class_name = "{}_class".format(vendor_name)
        parent_dir = os.path.dirname(__file__)
        vendor_module_path = os.path.join(parent_dir,"vendor","{}.py".format(vendor_class_name))
        # vendor_module = imp.load_source(vendor_class_name,vendor_module_path)

        # use importlib to dynamically load the module
        spec = importlib.util.spec_from_file_location(vendor_class_name,vendor_module_path)
        vendor_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(vendor_module)


        
        self.vendor_class = getattr(vendor_module, vendor_name)
        
        # Initialize the vendor and get missing items
        self.target_vendor = self.vendor_class(self.browser)
        self.missing = self.target_vendor.get_missing(self.target_vendor.vendor)
        self.total = len(self.missing)
        
        # Initialize the database and counter
        self.active_record = ActiveRecord()
        self.delay = 5
        self.counter = Counter()

    def run(self):
        # Open a backup file for failed scrapes
        backup_file = open(
            os.path.dirname(__file__)+"/helper/csv/outfile/{}_output_fail_safe.csv".format(self.target_vendor.vendor),
            "w"
        )
        backup_file_writer = csv.writer(backup_file)

        # Loop through missing items
        for sku in self.missing:
            print(sku)
            self.counter.subtotal += 1.0
            print("Progress: {}%".format(int((self.counter.subtotal / self.total) * 100)))

            # Search for item
            items = self.target_vendor.search_item(sku)

            if self.target_vendor.results(items):
                # Loop through results and scrape
                for item in items:
                    self.target_vendor.navigate(item)

                    db = self.target_vendor.get_info(sku)
                    time.sleep(self.delay)

                    # Save scraped data to database and backup file
                    if db is not None:
                        if isinstance(db, list):
                            print("Multiple items detected..")
                            for d in db:
                                if d is None:
                                    continue
                                self.active_record.save(d)
                                backup_file_writer.writerow(d.retrieve())
                        else:
                            self.active_record.save(db)
                            backup_file_writer.writerow(db.retrieve())
            else:
                # Directly attempt to get item info
                print("\nDirect get info attempt.\n")
                try:
                    db = self.target_vendor.get_info(sku)
                    time.sleep(self.delay)
                    if db is not None:
                        if isinstance(db, list):
                            print("Multiple items detected..")
                            for d in db:
                                self.active_record.save(d)
                                backup_file_writer.writerow(d.retrieve())
                        else:
                            print("Single item only..")
                            self.active_record.save(db)
                            backup_file_writer.writerow(db.retrieve())
                except:
                    print("Item not found.")

        # Close the backup file and wait before sending to database
        backup_file.close()
        time.sleep(3)

        # Send scraped data to file and close the browser
        self.target_vendor.send_to_file(self.target_vendor.vendor, self.active_record)
        print("Execution finished at: {}".format(datetime.now()))
        self.target_vendor.driver.close()


if __name__ == "__main__":
    vendor_name = sys.argv[1]
    scraper = Scraper(vendor_name)
    scraper.run()
    # os.system('shutdown -s') # This shuts down the computer.
