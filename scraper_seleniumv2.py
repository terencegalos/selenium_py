import csv,os,sys,time
from datetime import datetime

# Third-party libraries
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys

# Custom modules
from active_record import ActiveRecord
import webdriver_config


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
        vendor_class_name = "{}_class".format(vendor_name)
        vendor_module = __import__(vendor_class_name)
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
            os.path.dirname(__file__)+"./csv/outfile/{}_output_fail_safe.csv".format(self.target_vendor.vendor),
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